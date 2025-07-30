from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import Aula, NivelEducativo, Area, Asignatura, Grado, Grupo, PlanDeLeccion, Tema
from .forms import RegistroForm, LoginForm, NivelEducativoForm, GradoForm, GrupoForm, AreaForm, AsignaturaForm, TemasForm, PlanDeLeccionForm, aulaForm

# Create your views here.

#------------------INTERFAZ DE REGISTRO Y LOGIN----------------------
#sesion registro de usuarios
def vistaRegistro(request):
    form = RegistroForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Usuario registrado exitosamente')
        return redirect('registro')
    
    return render(request, 'registro.html', {'form': form} )

#Sesion login de usuarios
def VistaLogin(request):
    form = LoginForm(request.POST or None)
    if form.is_valid():
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')
        usuario = authenticate(request, email=email, password=password)
        if usuario is not None:
            login(request, usuario)
            messages.success(request, 'Inicio de sesion exitoso')
            return redirect("home")
        else:
            messages.error(request, 'Datos invalidos o no coinciden')
            return redirect('login')
    return render(request, 'login.html', {'form': form})

#------------------INTERFAZ PRINCIPAL-------------------------
def home(request):
    form = aulaForm()
    aulas = Aula.objects.all()
    return render(request, 'home.html', {'aulas': aulas, 'form': form})

#Seccion crear aula
def crearAula(request):
    form = aulaForm(request.POST or None)
    aulas = Aula.objects.all()
    if form.is_valid():
        form.save()
        messages.success(request, 'Aula creado con exito')
        return redirect('home')
    return render(request, 'home.html', {'form': form, 'aulas': aulas})

#Seccion eleiminar aula
def eliminarAula(request, pk):
    Aula.objects.get(pk=pk).delete()
    messages.success(request, 'Aula eliminada con exito')
    return redirect('home')


#---------VISTAS DE MENU DE HERRAMIENTAS DE SECCION PRINCIPAL--------
#Seccion niveles educativos
def vistaNivelEducativo(request):
    niveles = NivelEducativo.objects.all()
    return render(request, 'nivel_educativo.html', {'niveles': niveles})

#Seccion crear niveles educativos
def crearNivelEducativo(request):
    form = NivelEducativoForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Nivel edcuativo creado correctamente.')
        return redirect('nivel_educativo')
    return render(request, 'nivel_educativo')

#Seccion eliminar niveles educativos
def eliminarNivelEducativo(request, pk):
    NivelEducativo.objects.get(pk=pk).delete()
    messages.success(request, 'Nivel educativo eliminado exitosamente')
    return redirect('nivel_educativo')

#Seccion grados
def vistaGrados(request):
    form = GradoForm()
    grados = Grado.objects.all()
    return render(request, 'grados.html', {'grados': grados, 'form': form})

#Seccion Crear grados
def crearGrados(request): #PENDIENTE DE OBSERVACION NO ME INGRESA A UN TAMPLATE VACIO DE GRADOS Y AHI ES DONDE FUNCIONA EL FORMULARIO
    form = GradoForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Grado creado exitosamente')
        return redirect('grados')
    return render(request, 'grados.html', {'form': form})

#Seccion eliminar grados
def eliminarGrados(request, pk):
    Grado.objects.get(pk=pk).delete()
    messages.success(request, 'Grado eliminado exitosamente')
    return redirect('grados')

#Seccion grupos
def vistaGrupos(requets):
    form = GrupoForm()
    grupos = Grupo.objects.all()
    return render(requets, 'grupos.html', {'grupos': grupos, 'form': form})

#Seccion crear grupos
def crearGrupos(request):
    form = GrupoForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Grupo creado exitosamente')
        return redirect('grupos')
    return render(request, 'grupos.html', {'form': form})

#Seccion eliminar grupos
def eliminarGrupos(request, pk):
    Grupo.objects.get(pk=pk).delete()
    messages.success(request, 'Grupo eliminado exitosamente')
    return redirect('grupos')
    
#Seccion areas
def vistaAreas(request):
    form = AreaForm()
    areas = Area.objects.all()
    return render(request, 'areas.html', {'areas' : areas, 'form': form})

#Seccion crear area
def crearAreas(request):
    form = AreaForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Area creada exitosamente')
        return redirect('areas')
    return render(request, 'areas.html', {'form': form})

#Seccion eliminar area
def eliminarArea(request, pk):
    Area.objects.get(pk=pk).delete()
    messages.success(request, 'Area eliminada exitosamente')
    return redirect('areas')

#Seccion asignaturas
def vistaAsignaturas(request):
    form = AsignaturaForm()
    asignaturas = Asignatura.objects.all()
    return render(request, 'asignaturas.html', {'asignaturas': asignaturas, 'form': form})

#Seccion Crear asignaturas
def crearAsignaturas(request):
    form = AsignaturaForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Asignatura creada con exito')
        return redirect('asignaturas')
    return render('asignaturas', {'form': form})

#Seccion eliminar asignatura
def eliminarAsignatura(request, pk):
    Asignatura.objects.get(pk=pk).delete()
    messages.success(request, 'Asignatura eliminada exitosamente')
    return redirect('asignaturas')

#Seccion temas 
def vistaTemas(request):
    form = TemasForm()
    temas = Tema.objects.all()
    return render(request, 'temas.html', {'temas': temas, 'form': form})

#Seccion crear Temas
def crearTemas(request):
    form = TemasForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Tema creado exitosamente')
        return redirect('temas')
    return render('temas.html', {'form': form})

#Seccion eliminar temas
def eliminarTemas(request, pk):
    Tema.objects.get(pk=pk).delete()
    messages.success(request, 'Tema elimnado exitosamente')
    return redirect('temas')
    
#Seccion lista planes de leccion
def vistaPlanesLeccion(request):
    form = PlanDeLeccionForm()
    planes_leccion = PlanDeLeccion.objects.all()
    return render(request, 'planes_leccion.html', {'planes_leccion': planes_leccion, 'form': form})

#Seccion crear planes de leccion
def crearPlanDeLeccion(request):
    form = PlanDeLeccionForm(request.POST, request.FILES)
    if form.is_valid():
        form.save()
        print("Archivo guardado")
        messages.success(request, 'Plan de leccion creado exitosamente')
        return redirect('planes_leccion')
    return render(request, 'planes_leccion.html', {'form': form})

#Seccion eliminar plan de leccion
def eliminarPlanDeLeccion(request, pk):
    PlanDeLeccion.objects.get(pk=pk).delete()
    messages.success(request, 'Plan de leccion eliminado exitosamente')
    return redirect('planes_leccion')


#Seccion de interior de las aulas
def secc_aula(request, pk):
    aula = Aula.objects.get(pk=pk)
    asignaturas = aula.asignaturas.all()
    return render(request, 'secc_aula.html', {'aula': aula, 'asignaturas': asignaturas})

#Seccion desasignar asignatura de aula
def desasignarAsignatura(request, pk_aula, pk_asignatura):
    aula = Aula.objects.get(pk=pk_aula)
    asignatura = Asignatura.objects.get(pk=pk_asignatura)
    aula.asignaturas.remove(asignatura)
    messages.success(request, 'Asignatura desasignada exitosamente')
    return redirect('seccion_aula', pk=pk_aula)

def secc_asignaturas(request, pk):
    asignatura = Asignatura.objects.get(pk=pk)
    tema = asignatura.temas.all()
    return render(request, 'secc_asignaturas.html', {'asignatura': asignatura, 'tema': tema})




# Nota mental:
#     Las secciones como nivel educativo, grado, areas, temas y plan de leccion son
#     secciones predeterminadas por el desarrollador osea maneja un desplegable select 
#     En cambio grupos, Asignaturas y actividades son creadas por el coodinador o el docente