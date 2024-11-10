from django.urls import path
from . import views

urlpatterns = [
    path('', views.translate_pdf, name='translate_pdf'),
    path('download/', views.download_pdf, name='download_pdf')
]
