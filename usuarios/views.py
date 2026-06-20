from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages

@login_required
def lista_usuarios(request):
    usuarios = User.objects.all().order_by('id')
    return render(request, 'private/gestion_usuarios.html', {'usuarios': usuarios})

@login_required
def crear_usuario(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email', '')
        first_name = request.POST.get('first_name', '')
        last_name = request.POST.get('last_name', '')
        password = request.POST.get('password')
        is_staff = 'is_staff' in request.POST
        is_active = 'is_active' in request.POST

        if not username or not password:
            messages.error(request, "Usuario y contraseña son requeridos.")
            return redirect('usuarios:lista_usuarios')

        if User.objects.filter(username=username).exists():
            messages.error(request, f"El usuario '{username}' ya existe.")
            return redirect('usuarios:lista_usuarios')

        try:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
                is_staff=is_staff,
                is_active=is_active
            )
            messages.success(request, f"Usuario '{username}' creado exitosamente.")
        except Exception as e:
            messages.error(request, f"Error al crear usuario: {str(e)}")

    return redirect('usuarios:lista_usuarios')

@login_required
def editar_usuario(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email', '')
        first_name = request.POST.get('first_name', '')
        last_name = request.POST.get('last_name', '')
        password = request.POST.get('password')
        is_staff = 'is_staff' in request.POST
        is_active = 'is_active' in request.POST

        if not username:
            messages.error(request, "El nombre de usuario no puede estar vacío.")
            return redirect('usuarios:lista_usuarios')

        # Check if new username conflicts with another user
        if User.objects.filter(username=username).exclude(id=user_id).exists():
            messages.error(request, f"El usuario '{username}' ya está registrado.")
            return redirect('usuarios:lista_usuarios')

        try:
            user.username = username
            user.email = email
            user.first_name = first_name
            user.last_name = last_name
            user.is_staff = is_staff
            user.is_active = is_active
            if password:  # update password only if provided
                user.set_password(password)
            user.save()
            messages.success(request, f"Usuario '{username}' actualizado exitosamente.")
        except Exception as e:
            messages.error(request, f"Error al actualizar usuario: {str(e)}")

    return redirect('usuarios:lista_usuarios')

@login_required
def eliminar_usuario(request, user_id):
    user = get_object_or_404(User, id=user_id)
    # Prevent self-deletion for security
    if request.user.id == user.id:
        messages.error(request, "No puedes eliminar tu propio usuario en sesión.")
    else:
        try:
            username = user.username
            user.delete()
            messages.success(request, f"Usuario '{username}' eliminado exitosamente.")
        except Exception as e:
            messages.error(request, f"Error al eliminar usuario: {str(e)}")
            
    return redirect('usuarios:lista_usuarios')
