from django.urls import path
from . import views 

urlpatterns = [
    path('dispositivos/', views.dispositivos, name='dispositivos'),
    path('coisa/', views.coisa, name='coisa'),
    path('pandas/', views.pandas, name='pandas'),
]
