from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='app-odbrojuvanje'),
    path('novosti/', views.novosti, name='app-novosti'),
    path('novost?<novost_id>', views.otvorena_novost, name='app-otvorena-novost'),
    path('plasman/', views.plasman, name='app-plasman'),
    path('raspored/', views.raspored, name='app-raspored'),
    path('traka-info?<traka_id>', views.traka_info, name='app-traka-info'),
    path('gledaj/', views.gledaj, name='app-gledaj'),
    path('manage/', views.manage, name='app-manage'),
]

