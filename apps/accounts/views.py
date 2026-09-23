from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.views import View
from django.db.models import Q, Count
from datetime import date, timedelta
from django.utils import timezone
from .models import User
from .decorators import admin_required
from .forms import UserCreateForm, UserEditForm


class LoginView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect_by_role(request.user)
        return render(request, 'accounts/login.html')
    
    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if not user.actif:
                messages.error(request, "Votre compte est désactivé. Contactez l'administrateur.")
                return render(request, 'accounts/login.html')
            login(request, user)
            return redirect_by_role(user)
        messages.error(request, "Identifiants invalides")
        return render(request, 'accounts/login.html')


def redirect_by_role(user):
    """Redirige l'utilisateur vers la bonne page selon son rôle."""
    if user.is_admin_role():
        return redirect('accounts:gestion_utilisateurs')
    elif user.is_responsable():
        return redirect('accounts:gestion_utilisateurs')  # ou une vue responsable
    else:
        return redirect('carnet:liste_fiches')


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('accounts:login')


# ============================================================
# ADMINISTRATION DES UTILISATEURS (réservé aux admins)
# ============================================================

@admin_required
def gestion_utilisateurs(request):
    """Liste de tous les utilisateurs."""
    users = User.objects.all().order_by('role', 'username')
    
    q = request.GET.get('q', '').strip()
    if q:
        users = users.filter(
            Q(username__icontains=q) |
            Q(first_name__icontains=q) |
            Q(last_name__icontains=q) |
            Q(email__icontains=q)
        )
    
    role = request.GET.get('role')
    if role:
        users = users.filter(role=role)
    
    context = {
        'users': users,
        'q': q,
        'role_actif': role,
        'total': User.objects.count(),
        'nb_voyants': User.objects.filter(role='voyant').count(),
        'nb_responsables': User.objects.filter(role='responsable').count(),
        'nb_admins': User.objects.filter(role='admin').count(),
    }
    return render(request, 'accounts/gestion_utilisateurs.html', context)


@admin_required
def creation_utilisateur(request):
    """Créer un nouvel utilisateur."""
    if request.method == 'POST':
        form = UserCreateForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, f"Utilisateur '{user.nom_complet}' créé avec succès")
            return redirect('accounts:gestion_utilisateurs')
    else:
        form = UserCreateForm()
    
    return render(request, 'accounts/creation_utilisateur.html', {'form': form})


@admin_required
def detail_utilisateur(request, pk):
    """Vue admin : voir toutes les fiches, rappels, stats d'un utilisateur."""
    from apps.carnet.models import FicheClient, HistoriqueConsultation, RendezVous
    
    user_obj = get_object_or_404(User, pk=pk)
    
    fiches = FicheClient.objects.filter(voyant=user_obj).prefetch_related('historiques', 'rendezvous')
    
    total_fiches = fiches.count()
    total_historiques = HistoriqueConsultation.objects.filter(fiche__voyant=user_obj).count()
    total_rdv = RendezVous.objects.filter(fiche__voyant=user_obj).count()
    fiches_favorites = fiches.filter(favori=True).count()
    
    aujourdhui = date.today()
    rdv_a_venir = RendezVous.objects.filter(
        fiche__voyant=user_obj,
        date_rdv__gte=aujourdhui,
        statut__in=['planifie', 'confirme']
    ).select_related('fiche').order_by('date_rdv', 'heure_rdv')[:10]
    
    anniversaires = []
    for fiche in fiches.exclude(date_naissance=None):
        jours = fiche.anniversaire_dans
        if jours is not None and jours <= 30:
            anniversaires.append((fiche, jours))
    anniversaires.sort(key=lambda x: x[1])
    
    context = {
        'user_obj': user_obj,
        'fiches': fiches,
        'total_fiches': total_fiches,
        'total_historiques': total_historiques,
        'total_rdv': total_rdv,
        'fiches_favorites': fiches_favorites,
        'rdv_a_venir': rdv_a_venir,
        'anniversaires': anniversaires,
    }
    return render(request, 'accounts/detail_utilisateur.html', context)


@admin_required
def modification_utilisateur(request, pk):
    """Modifier un utilisateur existant."""
    user = get_object_or_404(User, pk=pk)
    
    if request.method == 'POST':
        form = UserEditForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, f"Utilisateur '{user.nom_complet}' modifié")
            return redirect('accounts:gestion_utilisateurs')
    else:
        form = UserEditForm(instance=user)
    
    return render(request, 'accounts/modification_utilisateur.html', {
        'form': form,
        'user_obj': user,
    })


@admin_required
def toggle_actif_utilisateur(request, pk):
    """Active/désactive un utilisateur."""
    user = get_object_or_404(User, pk=pk)
    if user == request.user:
        messages.error(request, "Vous ne pouvez pas désactiver votre propre compte.")
    else:
        user.actif = not user.actif
        user.save()
        etat = "activé" if user.actif else "désactivé"
        messages.success(request, f"Utilisateur {etat}")
    return redirect('accounts:gestion_utilisateurs')


@admin_required
def suppression_utilisateur(request, pk):
    """Supprimer un utilisateur."""
    user = get_object_or_404(User, pk=pk)
    
    if user == request.user:
        messages.error(request, "Vous ne pouvez pas supprimer votre propre compte.")
        return redirect('accounts:gestion_utilisateurs')
    
    if request.method == 'POST':
        nom = user.nom_complet
        user.delete()
        messages.success(request, f"Utilisateur '{nom}' supprimé")
        return redirect('accounts:gestion_utilisateurs')
    
    return render(request, 'accounts/suppression_utilisateur.html', {'user_obj': user})