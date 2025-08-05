from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from .models import Usuario, Pais, Departamento, Ciudad, Rol, TipoDocumento, NivelEducativo, Grado, Grupo, Area, Asignatura, Tema, Actividad, EntregaActividad, PlanDeLeccion, Aula, AsignarDocente

# Register your models here.

admin.site.register(Usuario)
admin.site.register(Pais)
admin.site.register(Departamento)
admin.site.register(Ciudad)
admin.site.register(Rol)
admin.site.register(TipoDocumento)
admin.site.register(NivelEducativo)
admin.site.register(Grado)
admin.site.register(Grupo)
admin.site.register(Area)
admin.site.register(Asignatura)
admin.site.register(Tema)
admin.site.register(Actividad)
admin.site.register(EntregaActividad)
admin.site.register(PlanDeLeccion)
admin.site.register(Aula)
admin.site.register(AsignarDocente)