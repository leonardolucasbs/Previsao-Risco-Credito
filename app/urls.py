from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('mostrar/', views.analise_credito, name='analise_credito'),
]
