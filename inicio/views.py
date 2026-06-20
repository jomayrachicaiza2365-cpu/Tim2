from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm

def inicio(request):
    return render(request, 'inicio.html')

def login_vista(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('inicio')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})
def acerca(request):
    return render(request, 'acerca.html')
def contacto(request):
    return render(request, 'contacto.html')