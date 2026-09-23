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
    
    # Historique
    path('historique/<int:pk>/modifier/', views.modifier_historique, name='modifier_historique'),
    path('historique/<int:pk>/supprimer/', views.supprimer_historique, name='supprimer_historique'),
    
    # Rendez-vous
    path('rdv/<int:pk>/statut/', views.changer_statut_rdv, name='changer_statut_rdv'),
    path('rdv/<int:pk>/modifier/', views.modifier_rdv, name='modifier_rdv'),
    path('rdv/<int:pk>/reporter/', views.reporter_rdv, name='reporter_rdv'),
    path('rdv/<int:pk>/supprimer/', views.supprimer_rdv, name='supprimer_rdv'),
    
    path('recherche/', views.recherche_ajax, name='recherche_ajax'),
    path('rappels/', views.rappels, name='rappels'),
    path('statistiques/', views.statistiques, name='statistiques'),
]