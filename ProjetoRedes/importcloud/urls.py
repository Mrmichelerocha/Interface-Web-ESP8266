from django.urls import path
from . import views 

urlpatterns = [
    path('database/', views.database, name='home'),
    path('form/', views.form, name='form'),
    path('create/', views.create, name='create'),
    path('view/<int:pk>/', views.view, name='view'),
    path('edit/<int:pk>/', views.edit, name='edit'),
    path('update/<int:pk>/', views.update, name='update'),
    path('delete/<int:pk>/', views.delete, name='delete'),
    path('importum/', views.importdb, name='importum'),
    path('importdois/', views.importdb2, name='importdois'),
]

