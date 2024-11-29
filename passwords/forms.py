# passwords/forms.py
from django import forms
from .models.passwordModel import Password

ENCRYPTION_CHOICES = [
    # ('bcrypt', 'Bcrypt'),
    # ('sha256', 'SHA-256'),
    ('fernet', 'Fernet'),
    ('aes', 'AES'),
]

class PasswordForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Contraseña'}),
        label='Contraseña'
    )
    encryption_method = forms.ChoiceField(
        choices=ENCRYPTION_CHOICES,
        initial='bcrypt',
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Método de Encriptación'
    )

    class Meta:
        model = Password
        fields = ['service', 'username', 'password', 'encryption_method']
        widgets = {
            'service': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Servicio'}),
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Usuario'}),
        }

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if len(password) < 6:
            raise forms.ValidationError("La contraseña debe tener al menos 6 caracteres.")
        return password

class CustomLoginForm(forms.Form):
    username = forms.CharField(
        label="Nombre de Usuario",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nombre de Usuario',
            'autofocus': True
        })
    )
    password = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Contraseña',
            'autocomplete': 'current-password'
        })
    )