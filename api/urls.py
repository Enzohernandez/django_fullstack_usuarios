"""
URL configuration for front project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from . import views
from django.contrib.auth.views import auth_login

urlpatterns = [
    ## GETS ##
    path("usuarios", views.get_usuarios, name=""),
    path("comentarios", views.get_posts, name=""),
    ## POSTS ##
    path("sign_up", views.sign_in, name=""),
    path("post", views.postear_comentario, name=""),
    path("prueba",views.sign_in_nuevo, name=""),
    path("desactivacion", views.desactivar_usuario, name=""),
    ## DELETE ##
    path("eliminar_usuarios", views.eliminar_usuario, name=""),
    path("eliminar_comentario", views.eliminar_comentario, name=""),
    ##  PUT ##
    path("modificar_usuario", views.modificar_usuario, name=""),
    path("modificar_comentario", views.modificar_post, name="")

]
#auth_login

