from .models import Usuario, Pais, Departamento, Ciudad, Rol, TipoDocumento
from django.urls import path, include
from .views import home, vistaNivelEducativo, vistaGrados, vistaGrupos, vistaAreas, vistaAsignaturas, vistaTemas, vistaPlanesLeccion, secc_aula
from .views import crearNivelEducativo, eliminarNivelEducativo, eliminarGrados, crearGrupos, crearAreas, eliminarArea, crearAsignaturas, eliminarAsignatura, crearTemas, eliminarTemas, crearPlanDeLeccion, eliminarPlanDeLeccion, crearAula, eliminarAula
from . import views

urlpatterns = [
    path('', home, name='home'),
    path('crear_aula/', views.crearAula, name='crear_aula'),
    path('eliminar_aula/<int:pk>', views.eliminarAula, name='eliminar_aula'),
#Secciones menu gestion educativa
    path('niveles_educativos/', vistaNivelEducativo, name='nivel_educativo'),
    path('niveles_educativos/crear_nivel/', views.crearNivelEducativo, name='crear_nivel_educativo'),
    path('niveles_educativos/eliminar_nivel/<int:pk>', views.eliminarNivelEducativo, name='eliminar_nivel'),
    path('grados/', vistaGrados, name='grados'),
    path('grados/crear_grado/', views.crearGrados, name='crear_grados'),
    path('grados/eliminar_grados/<int:pk>', views.eliminarGrados, name='eliminar_grado'),
    path('grupos/', vistaGrupos, name='grupos'),
    path('grupos/crear_grupos/', views.crearGrupos, name='crear_grupos'),
    path('grupos/eliminar_grupos/<int:pk>', views.eliminarGrupos, name='eliminar_grupo'),
    path('areas/', vistaAreas, name='areas'),
    path('areas/crear_areas', views.crearAreas, name='crear_areas'),
    path('areas/eliminar_areas/<int:pk>', views.eliminarArea, name='eliminar_areas'),
    path('asignaturas/', vistaAsignaturas, name='asignaturas'),
    path('asignaturas/crear_asignaturas/', views.crearAsignaturas, name='crear_asignatura'),
    path('asignaturas/eliminar_asignatura/<int:pk>', views.eliminarAsignatura, name='eliminar_asignatura'),
    path('temas/', vistaTemas, name='temas'),
    path('temas/crear_temas/', views.crearTemas, name='crear_temas'),
    path('temas/eliminar_temas/<int:pk>', views.eliminarTemas, name='eliminar_tema'),
    path('plan_leccion/', vistaPlanesLeccion, name='planes_leccion'),
    path('plan_leccion/crear_plan/', views.crearPlanDeLeccion, name='crear_plan'),
    path('plan_leccion/eliminar_plan/<int:pk>', views.eliminarPlanDeLeccion, name='eliminar_plan'),
#SECCION INTERIOR DE AULA
    path('aula/secc_aula/<int:pk>', secc_aula, name='seccion_aula')


]
