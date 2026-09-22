from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Count
from django.http import JsonResponse
from django.utils import timezone
from datetime import timedelta, date
from .models import FicheClient, HistoriqueConsultation, RendezVous
from .forms import (
    FicheClientForm, 
    HistoriqueConsultationForm, 
    RendezVousForm,
    RendezVousStatutForm,
)


@login_required
def liste_fiches(request):
    """Page d'accueil : toutes les fiches du voyant connecté"""
    fiches = FicheClient.objects.filter(voyant=request.user).prefetch_related('historiques', 'rendezvous')
    
    # Recherche
    q = request.GET.get('q', '').strip()
    if q:
        fiches = fiches.filter(
            Q(nom__icontains=q) |
            Q(prenom__icontains=q) |
            Q(telephone__icontains=q) |
            Q(email__icontains=q) |
            Q(description_generale__icontains=q) |
            Q(profession__icontains=q) |
            Q(lieu_naissance__icontains=q)
        )
    
    # Filtre favoris
    if request.GET.get('favori') == '1':
        fiches = fiches.filter(favori=True)
    
    # Filtre par tag
    tag = request.GET.get('tag')
    if tag:
        fiches = fiches.filter(tags__contains=[tag])
    
    # Tri
    tri = request.GET.get('tri', '-modifie_le')
    if tri in ['nom', '-nom', '-modifie_le', 'cree_le', '-cree_le']:
        fiches = fiches.order_by('-favori', tri)
    
    context = {
        'fiches': fiches,
        'q': q,
        'tag_actif': tag,
        'total': FicheClient.objects.filter(voyant=request.user).count(),
    }
    return render(request, 'carnet/liste_fiches.html', context)


@login_required
def detail_fiche(request, pk):
    """Vue détaillée d'une fiche client"""
    fiche = get_object_or_404(FicheClient, pk=pk, voyant=request.user)
    historiques = fiche.historiques.all()
    rendezvous = fiche.rendezvous.all()
    
    # Formulaire d'ajout d'historique
    if request.method == 'POST':
        form_type = request.POST.get('form_type')
        
        if form_type == 'historique':
            form = HistoriqueConsultationForm(request.POST)
            if form.is_valid():
                hist = form.save(commit=False)
                hist.fiche = fiche
                hist.save()
                fiche.save()
                messages.success(request, "Consultation ajoutée à l'historique")
                return redirect('carnet:detail_fiche', pk=fiche.pk)
        
        elif form_type == 'rdv':
            form_rdv = RendezVousForm(request.POST)
            if form_rdv.is_valid():
                rdv = form_rdv.save(commit=False)
                rdv.fiche = fiche
                rdv.save()
                messages.success(request, "Rendez-vous planifié")
                return redirect('carnet:detail_fiche', pk=fiche.pk)
    
    form_hist = HistoriqueConsultationForm()
    form_rdv = RendezVousForm(initial={'date_rdv': date.today()})
    form_statut = RendezVousStatutForm()
    
    context = {
    'fiche': fiche,
    'historiques': historiques,
    'rendezvous': rendezvous,
    'form_hist': form_hist,
    'form_rdv': form_rdv,
    'form_statut': form_statut,
    }
    return render(request, 'carnet/detail_fiche.html', context)


@login_required
def creation_fiche(request):
    if request.method == 'POST':
        form = FicheClientForm(request.POST)
        if form.is_valid():
            fiche = form.save(commit=False)
            fiche.voyant = request.user
            fiche.save()
            messages.success(request, f"Fiche de {fiche.nom_complet} créée")
            return redirect('carnet:detail_fiche', pk=fiche.pk)
    else:
        form = FicheClientForm()
    
    return render(request, 'carnet/creation_fiche.html', {'form': form})


@login_required
def modification_fiche(request, pk):
    fiche = get_object_or_404(FicheClient, pk=pk, voyant=request.user)
    
    if request.method == 'POST':
        form = FicheClientForm(request.POST, instance=fiche)
        if form.is_valid():
            form.save()
            messages.success(request, "Fiche modifiée")
            return redirect('carnet:detail_fiche', pk=fiche.pk)
    else:
        form = FicheClientForm(instance=fiche)
    
    return render(request, 'carnet/modification_fiche.html', {'form': form, 'fiche': fiche})


@login_required
def suppression_fiche(request, pk):
    fiche = get_object_or_404(FicheClient, pk=pk, voyant=request.user)
    if request.method == 'POST':
        nom = fiche.nom_complet
        fiche.delete()
        messages.success(request, f"Fiche de {nom} supprimée")
        return redirect('carnet:liste_fiches')
    return render(request, 'carnet/suppression_fiche.html', {'fiche': fiche})


@login_required
def toggle_favori(request, pk):
    fiche = get_object_or_404(FicheClient, pk=pk, voyant=request.user)
    fiche.favori = not fiche.favori
    fiche.save()
    return JsonResponse({'favori': fiche.favori})


@login_required
def recherche_ajax(request):
    """Recherche instantanée en AJAX"""
    q = request.GET.get('q', '').strip()
    fiches = FicheClient.objects.filter(voyant=request.user)
    if q:
        fiches = fiches.filter(
            Q(nom__icontains=q) | Q(prenom__icontains=q) |
            Q(telephone__icontains=q) | Q(email__icontains=q) |
            Q(profession__icontains=q)
        )[:20]
    else:
        fiches = fiches.order_by('-favori', '-modifie_le')[:20]
    
    return render(request, 'carnet/partials/grille_fiches.html', {'fiches': fiches})


@login_required
def rappels(request):
    """Rappels : anniversaires, RDV à venir, clients inactifs"""
    aujourdhui = date.today()
    fiches = FicheClient.objects.filter(voyant=request.user)
    
    # Anniversaires dans les 30 prochains jours
    anniversaires = []
    for fiche in fiches.exclude(date_naissance=None):
        jours = fiche.anniversaire_dans
        if jours is not None and jours <= 30:
            anniversaires.append((fiche, jours))
    anniversaires.sort(key=lambda x: x[1])
    
    # RDV à venir (les 30 prochains jours)
    rdv_a_venir = RendezVous.objects.filter(
        fiche__voyant=request.user,
        date_rdv__gte=aujourdhui,
        date_rdv__lte=aujourdhui + timedelta(days=30),
        statut__in=['planifie', 'confirme']
    ).select_related('fiche').order_by('date_rdv', 'heure_rdv')
    
    # Fiches inactives
    limite = timezone.now() - timedelta(days=60)
    inactifs = fiches.filter(modifie_le__lt=limite)[:10]
    
    context = {
        'anniversaires': anniversaires,
        'rdv_a_venir': rdv_a_venir,
        'inactifs': inactifs,
    }
    return render(request, 'carnet/rappels.html', context)


@login_required
def statistiques(request):
    fiches = FicheClient.objects.filter(voyant=request.user)
    
    total_fiches = fiches.count()
    total_historiques = HistoriqueConsultation.objects.filter(fiche__voyant=request.user).count()
    total_rdv = RendezVous.objects.filter(fiche__voyant=request.user).count()
    fiches_favorites = fiches.filter(favori=True).count()
    
    # Répartition par sexe
    repartition_sexe = {
        'Hommes': fiches.filter(sexe='M').count(),
        'Femmes': fiches.filter(sexe='F').count(),
        'Autres': fiches.filter(sexe='A').count(),
        'Non_renseigne': fiches.filter(sexe='').count(),
    }
    
    # Répartition par signe astrologique
    signes_data = {}
    for fiche in fiches.exclude(signe_astrologique=''):
        signes_data[fiche.signe_astrologique] = signes_data.get(fiche.signe_astrologique, 0) + 1
    
    # Répartition par forfait
    forfaits_data = {}
    for fiche in fiches.exclude(forfait=''):
        label = fiche.forfait_label
        forfaits_data[label] = forfaits_data.get(label, 0) + 1
    
    # Statistiques RDV - COMPTAGE DIRECT PAR STATUT
    rdv_par_statut = {
        'Planifies': RendezVous.objects.filter(fiche__voyant=request.user, statut='planifie').count(),
        'Confirmes': RendezVous.objects.filter(fiche__voyant=request.user, statut='confirme').count(),
        'Termines': RendezVous.objects.filter(fiche__voyant=request.user, statut='termine').count(),
        'Reportes': RendezVous.objects.filter(fiche__voyant=request.user, statut='reporte').count(),
        'Annules': RendezVous.objects.filter(fiche__voyant=request.user, statut='annule').count(),
    }
    
    # Consultations par mois (6 derniers mois)
    from datetime import date, timedelta
    from django.db.models.functions import TruncMonth
    six_mois = date.today() - timedelta(days=180)
    consultations_par_mois = (
        HistoriqueConsultation.objects
        .filter(fiche__voyant=request.user, date_consultation__gte=six_mois)
        .annotate(mois=TruncMonth('date_consultation'))
        .values('mois')
        .annotate(total=Count('id'))
        .order_by('mois')
    )
    mois_labels = []
    mois_values = []
    mois_fr = ['Jan', 'Fév', 'Mar', 'Avr', 'Mai', 'Juin', 'Juil', 'Août', 'Sep', 'Oct', 'Nov', 'Déc']
    for item in consultations_par_mois:
        if item['mois']:
            mois_labels.append(f"{mois_fr[item['mois'].month - 1]} {item['mois'].year}")
            mois_values.append(item['total'])
    
    context = {
        'total_fiches': total_fiches,
        'total_historiques': total_historiques,
        'total_rdv': total_rdv,
        'fiches_favorites': fiches_favorites,
        'repartition_sexe': repartition_sexe,
        'signes_data': signes_data,
        'forfaits_data': forfaits_data,
        'rdv_par_statut': rdv_par_statut,
        'mois_labels': mois_labels,
        'mois_values': mois_values,
    }
    return render(request, 'carnet/statistiques.html', context)

@login_required
def changer_statut_rdv(request, pk):
    """Change le statut d'un RDV après qu'il soit passé."""
    rdv = get_object_or_404(
        RendezVous, 
        pk=pk, 
        fiche__voyant=request.user
    )
    
    if not rdv.est_passe:
        messages.error(request, "Ce rendez-vous n'est pas encore passé.")
        return redirect('carnet:detail_fiche', pk=rdv.fiche.pk)
    
    if request.method == 'POST':
        form = RendezVousStatutForm(request.POST, instance=rdv)
        if form.is_valid():
            form.save()
            messages.success(request, f"Statut du RDV mis à jour : {rdv.get_statut_display()}")
            return redirect('carnet:detail_fiche', pk=rdv.fiche.pk)
    else:
        form = RendezVousStatutForm(instance=rdv)
    
    return render(request, 'carnet/changer_statut_rdv.html', {
        'rdv': rdv,
        'form': form,
    })