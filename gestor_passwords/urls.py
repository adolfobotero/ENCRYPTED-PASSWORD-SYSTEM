"""gestor_passwords URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from passwords.views import passwordView
from passwords.views import loginView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', loginView.user_login, name='login'),
    path('logout/', loginView.user_logout, name='logout'),
    path('', passwordView.password_list, name='password_list'),
    path('add/', passwordView.add_password, name='add_password'),
    path('view/<int:pk>/', passwordView.view_password, name='view_password'),
    path('delete/<int:pk>/', passwordView.delete_password, name='delete_password'),
]