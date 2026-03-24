from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from .models import Laboratorio, Usuario, RegistroBitacora
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from datetime import datetime

# --- AUXILIAR DE SEGURIDAD ---
def obtener_usuario(request):
    user_id = request.session.get('usuario_id')
    if user_id:
        try:
            return Usuario.objects.get(id=user_id)
        except Usuario.DoesNotExist:
            return None
    return None

# --- NAVEGACIÓN Y AUTENTICACIÓN ---
def home(request):
    return render(request, 'index.html')

def dashboard(request):
    user = obtener_usuario(request)
    if not user: 
        return redirect('login')
    
    # Conteo dinámico para las tarjetas del Dashboard
    total_labs = Laboratorio.objects.count()
    total_maestros = Usuario.objects.filter(rol='docente').count()

    context = {
        'rol': user.rol,
        'total_labs': total_labs,
        'total_maestros': total_maestros
    }
    
    return render(request, 'dashboard.html', context)

def iniciar_sesion(request):
    if request.method == 'POST':
        correo_login = request.POST.get('correo')
        pass_login = request.POST.get('password')
        try:
            user = Usuario.objects.get(correo=correo_login)
            if check_password(pass_login, user.password):
                request.session['usuario_id'] = user.id
                request.session['usuario_nombre'] = user.nombre
                return redirect('dashboard')
            else:
                messages.error(request, "Contraseña incorrecta.")
        except Usuario.DoesNotExist:
            messages.error(request, "Este correo no está registrado.")
    return render(request, 'login.html')

def cerrar_sesion(request):
    request.session.flush()
    return redirect('login')

# --- GESTIÓN DE USUARIOS (SOLO ADMIN) ---
def usuarios(request):
    user = obtener_usuario(request)
    if not user or user.rol != 'admin':
        messages.error(request, "Acceso denegado.")
        return redirect('dashboard')
    return render(request, 'usuarios.html', {'usuarios': Usuario.objects.all(), 'rol': user.rol})

def agregar_usuario(request):
    user = obtener_usuario(request)
    if not user or user.rol != 'admin': return redirect('dashboard')
    
    if request.method == 'POST':
        nom = request.POST.get('nombre_completo')
        con = request.POST.get('correo')
        rol = request.POST.get('rol')
        pas = request.POST.get('password')
        Usuario.objects.create(nombre=nom, correo=con, rol=rol, password=make_password(pas))
        messages.success(request, f"Usuario {nom} registrado.")
        return redirect('usuarios')
    return render(request, 'agregar-usuario.html', {'rol': user.rol})

def editar_usuario(request, id):
    user = obtener_usuario(request)
    if not user or user.rol != 'admin': return redirect('dashboard')
    
    usuario_edit = get_object_or_404(Usuario, id=id)
    if request.method == 'POST':
        usuario_edit.nombre = request.POST.get('nombre_completo')
        usuario_edit.correo = request.POST.get('correo')
        usuario_edit.rol = request.POST.get('rol')
        usuario_edit.save()
        messages.success(request, "Usuario actualizado.")
        return redirect('usuarios')
    return render(request, 'editar-usuario.html', {'usuario': usuario_edit, 'rol': user.rol})

def eliminar_usuario(request, id):
    user = obtener_usuario(request)
    if not user or user.rol != 'admin': return redirect('dashboard')
    get_object_or_404(Usuario, id=id).delete()
    messages.success(request, "Usuario eliminado.")
    return redirect('usuarios')

# --- GESTIÓN DE LABORATORIOS (SOLO ADMIN) ---
def laboratorios(request):
    user = obtener_usuario(request)
    if not user or user.rol != 'admin':
        messages.error(request, "Acceso denegado.")
        return redirect('dashboard')
    return render(request, 'laboratorios.html', {'laboratorios': Laboratorio.objects.all(), 'rol': user.rol})

def nuevo_laboratorio(request):
    user = obtener_usuario(request)
    if not user or user.rol != 'admin': return redirect('dashboard')
    
    if request.method == 'POST':
        Laboratorio.objects.create(
            nombre=request.POST.get('nombre'), 
            ubicacion=request.POST.get('ubicacion')
        )
        messages.success(request, "Laboratorio registrado.")
        return redirect('laboratorios')
    return render(request, 'nuevo-laboratorio.html', {'rol': user.rol})

def editar_laboratorio(request, id):
    user = obtener_usuario(request)
    if not user or user.rol != 'admin': return redirect('dashboard')
    
    lab = get_object_or_404(Laboratorio, id=id)
    if request.method == 'POST':
        lab.nombre = request.POST.get('nombre')
        lab.ubicacion = request.POST.get('ubicacion')
        lab.save()
        messages.success(request, "Laboratorio actualizado.")
        return redirect('laboratorios')
    return render(request, 'editar-laboratorio.html', {'laboratorio': lab, 'rol': user.rol})

def eliminar_laboratorio(request, id):
    user = obtener_usuario(request)
    if not user or user.rol != 'admin': return redirect('dashboard')
    get_object_or_404(Laboratorio, id=id).delete()
    messages.success(request, "Laboratorio eliminado.")
    return redirect('laboratorios')

# --- BITÁCORA ---
def bitacora(request):
    user = obtener_usuario(request)
    if not user: return redirect('login')
    
    if request.method == 'POST':
        # Capturamos la carrera seleccionada en el modal de bitacora.html
        carrera_post = request.POST.get('carrera')
        
        RegistroBitacora.objects.create(
            docente=user,
            laboratorio_id=request.POST.get('laboratorio'),
            carrera=carrera_post,
            grado_grupo=request.POST.get('grado_grupo'),
            anio=request.POST.get('anio', 2026),
            fecha=request.POST.get('fecha'),
            hora_entrada=request.POST.get('hora_entrada'),
            hora_salida=request.POST.get('hora_salida'),
            equipo=request.POST.get('equipo'),
            observaciones=request.POST.get('observaciones', '')
        )
        messages.success(request, "Registro de bitácora guardado.")
        return redirect('bitacora')

    registros = RegistroBitacora.objects.filter(docente=user).order_by('-fecha')
    return render(request, 'bitacora.html', {
        'registros': registros,
        'laboratorios': Laboratorio.objects.all(),
        'rol': user.rol,
        'nombre_docente': user.nombre
    })

def exportar_pdf_bitacora(request):
    user = obtener_usuario(request)
    if not user: 
        return redirect('login')
    
    # Obtenemos los registros y la fecha actual
    registros = RegistroBitacora.objects.filter(docente=user).order_by('-fecha')
    fecha_actual = datetime.now().strftime("%d/%m/%Y")
    
    context = {
        'docente': user.nombre,
        'registros': registros,
        'fecha_hoy': fecha_actual
    }
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="Bitacora_{user.nombre}.pdf"'
    
    template = get_template('pdf_templates.html') 
    html = template.render(context)
    
    pisa_status = pisa.CreatePDF(html, dest=response)
    
    if pisa_status.err:
        return HttpResponse('Error al generar PDF', status=500)
        
    return response