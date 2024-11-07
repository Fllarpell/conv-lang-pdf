from django.urls import path
from . import views

urlpatterns = [
    path('', views.translate_pdf, name='translate_pdf'),
]
