from django.urls import path
from . import views

app_name = 'carnet'

urlpatterns = [
    path('', views.liste_fiches, name='liste_fiches'),
    path('nouvelle/', views.creation_fiche, name='creation_fiche'),
    path('fiche/<int:pk>/', views.detail_fiche, name='detail_fiche'),
    path('fiche/<int:pk>/modifier/', views.modification_fiche, name='modification_fiche'),
    path('fiche/<int:pk>/supprimer/', views.suppression_fiche, name='suppression_fiche'),
    path('fiche/<int:pk>/favori/', views.toggle_favori, name='toggle_favori'),
    path('recherche/', views.recherche_ajax, name='recherche_ajax'),
    path('rappels/', views.rappels, name='rappels'),
    path('statistiques/', views.statistiques, name='statistiques'),
]