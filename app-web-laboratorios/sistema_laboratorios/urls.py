from django.contrib import admin
from django.urls import path
from core import views 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.iniciar_sesion, name='home'), 
    path('login/', views.iniciar_sesion, name='login'),
    path('logout/', views.cerrar_sesion, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('usuarios/', views.usuarios, name='usuarios'),
    path('usuarios/nuevo/', views.agregar_usuario, name='agregar_usuario'),
    path('usuarios/editar/<int:id>/', views.editar_usuario, name='editar_usuario'),
    path('usuarios/eliminar/<int:id>/', views.eliminar_usuario, name='eliminar_usuario'),
    path('laboratorios/', views.laboratorios, name='laboratorios'),
    path('laboratorios/nuevo/', views.nuevo_laboratorio, name='nuevo_laboratorio'),
    # --- RUTA AÑADIDA PARA EDITAR ---
    path('laboratorios/editar/<int:id>/', views.editar_laboratorio, name='editar_laboratorio'),
    path('laboratorios/eliminar/<int:id>/', views.eliminar_laboratorio, name='eliminar_laboratorio'),
    path('bitacora/', views.bitacora, name='bitacora'),
    path('bitacora/pdf/', views.exportar_pdf_bitacora, name='descargar_pdf_bitacora'),
]