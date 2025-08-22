from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group, Permission, User
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.utils import timezone
# Create your models here.

#------------------SECCION DE CREACION Y REGISTRO DE USUARIO----------
# DATOS BASE DE REGISTRO (ABSTRACTO)
class UsuarioBase(models.Model):
    primer_nombre = models.CharField(max_length=30)
    segundo_nombre = models.CharField(max_length=30, blank=True)
    primer_apellido = models.CharField(max_length=30)
    segundo_apellido = models.CharField(max_length=30)
    fecha_nacimiento = models.DateField()
    
    class Meta:
        abstract = True
    
    def __str__(self):
        return f'{self.primer_nombre} {self.segundo_nombre} {self.primer_apellido} {self.segundo_apellido}'

#REGISTRAR USUARIO Y SUPER USUARIO
class UsuarioManager(BaseUserManager):
    def crear_usuario(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Ingresar correo electronico')
        email = self.normalize_email(email)
        usuario = self.model(email=email, **extra_fields)
        usuario.set_password(password)
        usuario.save(using=self._db)
        return usuario
    
    def create_superuser(self, email, password=None, **extra_fields):#Metodo para crear superusuario
        rol_admin, _ = Rol.objects.get_or_create(rol='Administrador')
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields['rol']= rol_admin
        return self.crear_usuario(email, password, **extra_fields)

# DATOS PRINCIPALES DE VALIDACION DE USUARIO
class Usuario(AbstractBaseUser, PermissionsMixin):
    rol = models.ForeignKey('Rol', on_delete=models.PROTECT)
    email = models.EmailField(unique=True)
    
    tipo_documento = models.ForeignKey('TipoDocumento', on_delete=models.PROTECT, null=True)
    numero_documento = models.CharField(max_length=15, unique=True)
    
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    objects = UsuarioManager()
    
    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
    
    def __str__(self):
        return f'{self.email}, {self.tipo_documento}, {self.numero_documento}'


#----------------------------------------------------------------
    
# DATOS DE UBICACION DE USUARIO
class Pais(models.Model):
    pais = models.CharField(max_length=50)
    
    def __str__(self):
        return f'{self.pais}'
    
class Departamento(models.Model):
    departamento = models.CharField(max_length=40)
    pais = models.ForeignKey(Pais, on_delete=models.PROTECT)
    
    def __str__(self):
        return f'{self.departamento}'
    
class Ciudad(models.Model):
    ciudad = models.CharField(max_length=40)
    departamtento = models.ForeignKey(Departamento, on_delete=models.PROTECT)
    
    def __str__(self):
        return f'{self.ciudad}'
    
# ROLES DE USUARIOS
class Rol(models.Model):
    rol = models.CharField(max_length=20)
    
    def __str__(self):
        return f'{self.rol}'
    
# TIPO DE DOCUMENTO PARA USUARIO
class TipoDocumento(models.Model):
    tipo_documento = models.CharField(max_length=20)
    
    def __str__(self):
        return f"{self.tipo_documento}"
    
    #-------SECCION DE CREACION DE SECCIONES EDUCATIVAS
    
#CREACION DE NIVELES EDUCATIVOS
class NivelEducativo(models.Model):
    nivel = models.CharField(max_length=30, unique=True, null=False, blank=False)
    
    def __str__(self):
        return f"{self.nivel}"
    
#CREACION DE GRADOS DEL COLEGIO
class Grado(models.Model):
    grado = models.CharField(max_length=15)
    nivel_educativo = models.ForeignKey(NivelEducativo, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.grado}"

#GRUPO QUE SE LE ASIGNA AL GRADO
class Grupo(models.Model):
    grupo = models.CharField(max_length=10)
    grado_asignado = models.ForeignKey(Grado, unique=False, on_delete=models.CASCADE)
    
    class Meta:
        unique_together = ('grado_asignado','grupo')
    
    def __str__(self):
        return f"{self.grupo}"


#CREACION DE AREAS
class Area(models.Model):
    area = models.CharField(max_length=50, unique=True)
    
    def __str__(self):
        return f"{self.area}"
    
#CREACION DE ASIGNATURAS
class Asignatura(models.Model):
    asignatura = models.CharField(max_length=50)
    area_asignada = models.ForeignKey(Area, on_delete=models.CASCADE)
    grado_asignado = models.ForeignKey(Grado, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"({self.grado_asignado}) - {self.asignatura}"
    
#CREACION DE TEMAS
class Tema(models.Model):
    tema = models.CharField(max_length=50)
    asignatura_asignada = models.ForeignKey(Asignatura, on_delete=models.CASCADE, related_name='temas')
    
    def __str__(self):
        return f"{self.tema}"
    
#CREACION DE ACTIVIDADES (Funcion exclusiva para docentes)
class Actividad(models.Model):
    actividad = models.CharField(max_length=50)
    tema_asignado = models.ForeignKey(Tema, on_delete=models.CASCADE)
    descripcion = models.TextField(blank=True)
    fecha_entrega = models.DateField()
    archivo = models.FileField(upload_to='actividades/', blank=True, null=True)
    
    def __str__(self):
        return f"{self.actividad}"
    
#TABLA DE EVIDENCIAS DE ALUMNOS 
class EntregaActividad(models.Model): 
    actividad_asignada = models.ForeignKey(Actividad, on_delete=models.CASCADE)
    estudiante = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    archivo_entregado = models.FileField(upload_to='entregas/')
    calificacion = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    observacion = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.actividad_asignada}"
    

# CREACION DE PLANES DE LECCION TIPO PDF
class PlanDeLeccion(models.Model):
    plan_leccion = models.CharField(max_length=40)
    area = models.ForeignKey(Area, on_delete=models.CASCADE)
    tema = models.ForeignKey(Tema, on_delete=models.CASCADE)
    archivo_plan = models.FileField(upload_to='planesDeLeccion/', null=True, blank=True)
    
    def __str__(self):
        return f"{self.plan_leccion}"
    
    
# CREACION DE AULAS
class Aula(models.Model):
    grado = models.ForeignKey(Grado, on_delete=models.CASCADE)
    grupo = models.ForeignKey(Grupo, on_delete=models.CASCADE)
    asignaturas = models.ManyToManyField(Asignatura)  # 🔄 Una aula puede tener varias asignaturas

    def __str__(self):
        return f"{self.grado}- {self.grupo}"

#asignar docente a asignatura
class AsignarDocente(models.Model):
    docente = models.ForeignKey(Usuario, on_delete=models.CASCADE, limit_choices_to={'rol__rol':'Docente'})
    asignatura = models.ForeignKey(Asignatura, on_delete=models.CASCADE)
    aula = models.ForeignKey(Aula, on_delete=models.CASCADE)
    
    class Meta:
        unique_together = ('asignatura', 'aula')
        
    def __str__(self):
        return f"{self.docente} - {self.asignatura} ({self.aula})"