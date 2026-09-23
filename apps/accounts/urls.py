from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    
    # Gestion des utilisateurs (admin seulement)
    path('utilisateurs/', views.gestion_utilisateurs, name='gestion_utilisateurs'),
    path('utilisateurs/nouveau/', views.creation_utilisateur, name='creation_utilisateur'),
    path('utilisateurs/<int:pk>/modifier/', views.modification_utilisateur, name='modification_utilisateur'),
    path('utilisateurs/<int:pk>/toggle/', views.toggle_actif_utilisateur, name='toggle_actif_utilisateur'),
    path('utilisateurs/<int:pk>/supprimer/', views.suppression_utilisateur, name='suppression_utilisateur'),
]