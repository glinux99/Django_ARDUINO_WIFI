
from django.urls import path, re_path
from . import views
import re
urlpatterns = [
    path('', views.HomeP, name='HomePage'),
    path('<int:lampe>/', views.HomeP1, name='HomeP1'),
    path('connect/<int:lampe>/', views.Connect, name='connect'),
    path('lampes/', views.Lampes, name='lampes'),
    path('securite/', views.securite, name='security'),
    path('PlanSmartHome/', views.Lampes, name='planHome'),
    path('automatisation/', views.auto, name='auto'),
    path('autres/', views.autres, name='autres'),
    path('statistiques/', views.statistiques, name='statistiques'),
    path('autorisations/', views.autorisations, name='autorisations'),
    path('fermer/', views.fermer, name='fermer'),
    path('essaie/', views.essaie, name='essaie'),
]
