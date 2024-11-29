# views.py
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from ..models.passwordModel import Password
from django.contrib.auth import logout
from ..forms import CustomLoginForm

def user_logout(request):
    logout(request)
    return redirect('login')

def user_login(request):
    if request.method == 'POST':
        # form = AuthenticationForm(request, data=request.POST)
        # if form.is_valid():
        #     username = form.cleaned_data.get('username')
        #     password = form.cleaned_data.get('password')
        #     user = authenticate(request, username=username, password=password)
        #     if user is not None:
        #         login(request, user)
        #         messages.success(request, f"¡Bienvenido, {username}!")
        #         passwords = Password.objects.all()
        #         return render(request, 'passwords/password_list.html', {'passwords': passwords})
        #         # return redirect('home')  # Redirige a la página de inicio o cualquier otra
        #     else:
        #         messages.error(request, "Usuario o contraseña incorrectos.")

        form = CustomLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                # messages.success(request, f"¡Bienvenido, {username}!")
                passwords = Password.objects.all()
                return render(request, 'passwords/password_list.html', {'passwords': passwords})
            else:
                messages.error(request, "Usuario o contraseña incorrectos.")
        else:
            messages.error(request, "Formulario no válido.")
    else:
        form = AuthenticationForm()
    
    return render(request, 'passwords/login.html', {'form': form})
