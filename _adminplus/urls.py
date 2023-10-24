from django.urls import path
from . import views

app_name = '_adminplus'

urlpatterns = [
    path('adminplus/', views.adminplus, name='adminplus'),
]
