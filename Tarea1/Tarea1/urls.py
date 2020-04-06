"""Tarea1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from Tarea1.views import home, episodio, personaje, lugar, buscar



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name = "home"),
    path('episodio/<int:identificador>',episodio, name = "episodio"),
    path('personaje/<int:identificador>',personaje, name = "personaje"),
    path('lugar/<int:id_lugar>',lugar, name = "lugar"),
    path('buscar/',buscar, name = "buscar"),
    path('episodio/buscar/',buscar, name = "buscar"),
    path('personaje/buscar/',buscar, name = "buscar"),
    path('lugar/buscar/',buscar, name = "buscar")
]
