# passwords/views.py

from django.shortcuts import render, redirect, get_object_or_404
from .models.passwordModel import Password
from .forms import PasswordForm

def password_list(request):
    passwords = Password.objects.all()
    return render(request, 'passwords/password_list.html', {'passwords': passwords})

def add_password(request):
    if request.method == 'POST':
        form = PasswordForm(request.POST)
        if form.is_valid():
            password_instance = form.save(commit=False)
            password_instance.set_password(form.cleaned_data['password'])
            password_instance.save()
            return redirect('password_list')
    else:
        form = PasswordForm()
    return render(request, 'passwords/add_password.html', {'form': form})

def view_password(request, pk):
    password = get_object_or_404(Password, pk=pk)
    
    # Cambiar get_password por get_decrypted_password
    try:
        decrypted_password = password.get_decrypted_password()
    except ValueError as e:
        decrypted_password = str(e)  # Mensaje de error si la encriptación no soporta desencriptación

    return render(request, 'passwords/view_password.html', {
        'password': password,
        'decrypted_password': decrypted_password,
    })

def delete_password(request, pk):
    password = get_object_or_404(Password, pk=pk)
    if request.method == 'POST':
        password.delete()
        return redirect('password_list')
    return render(request, 'passwords/password_list.html')