from django.urls import path
from . import views

app_name = 'chatapp'

urlpatterns = [
    path('gledaj/', views.gledaj, name='chatapp-gledaj'),
    path('send/', views.send, name='chatapp-send'),
    path('getMessages/', views.getMessages, name='getMessages'),
]