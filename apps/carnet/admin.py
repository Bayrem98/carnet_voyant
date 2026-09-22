from django.contrib import admin
from .models import FicheClient, HistoriqueConsultation, RendezVous


@admin.register(FicheClient)
class FicheClientAdmin(admin.ModelAdmin):
    list_display = (
        'nom_complet', 'voyant', 'telephone', 'sexe',
        'date_naissance', 'signe_astrologique', 'favori', 'forfait', 'modifie_le'
    )
    list_filter = ('favori', 'forfait', 'sexe', 'voyant', 'cree_le')
    search_fields = ('nom', 'prenom', 'telephone', 'email')
    readonly_fields = ('chemin_de_vie', 'annee_personnelle', 'chiffre_cle', 'signe_astrologique')
    date_hierarchy = 'cree_le'


@admin.register(HistoriqueConsultation)
class HistoriqueConsultationAdmin(admin.ModelAdmin):
    list_display = ('fiche', 'date_consultation', 'titre', 'duree_minutes', 'cree_le')
    list_filter = ('date_consultation', 'cree_le')
    search_fields = ('titre', 'notes_generales', 'sujet_sentimental',
                     'sujet_professionnel', 'sujet_financier')
    date_hierarchy = 'date_consultation'


@admin.register(RendezVous)
class RendezVousAdmin(admin.ModelAdmin):
    list_display = ('fiche', 'date_rdv', 'heure_rdv', 'mode', 'statut', 'duree_estimee')
    list_filter = ('statut', 'mode', 'date_rdv')
    search_fields = ('fiche__nom', 'fiche__prenom', 'sujet_prevu', 'notes')
    date_hierarchy = 'date_rdv'