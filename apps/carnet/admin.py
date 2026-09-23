from django.contrib import admin
from .models import FicheClient, HistoriqueConsultation, RendezVous


@admin.register(FicheClient)
class FicheClientAdmin(admin.ModelAdmin):
    list_display = (
        'nom_complet', 'voyant', 'telephone', 'sexe',
        'date_naissance', 'signe_astrologique', 'favori', 'forfait', 'modifie_le'
    )
    list_filter = ('favori', 'forfait', 'sexe', 'voyant', 'cree_le')
    search_fields = ('nom', 'prenom', 'telephone', 'email', 'description_generale')
    readonly_fields = ('chemin_de_vie', 'annee_personnelle', 'chiffre_cle',
                      'signe_astrologique', 'cree_le', 'modifie_le')
    date_hierarchy = 'cree_le'
    list_per_page = 30
    
    fieldsets = (
        ('Voyant propriétaire', {
            'fields': ('voyant',)
        }),
        ('Identité du client', {
            'fields': ('nom', 'prenom', 'sexe', 'telephone', 'email')
        }),
        ('Naissance', {
            'fields': ('date_naissance', 'lieu_naissance', 'signe_astrologique')
        }),
        ('Numérologie', {
            'fields': ('chemin_de_vie', 'annee_personnelle', 'chiffre_cle'),
            'classes': ('collapse',),
        }),
        ('Vie personnelle', {
            'fields': ('situation_familiale', 'profession', 'nombre_enfants')
        }),
        ('Forfait', {
            'fields': ('forfait', 'forfait_minutes_utilisees', 'forfait_notes')
        }),
        ('Description', {
            'fields': ('description_generale',)
        }),
        ('Organisation', {
            'fields': ('tags', 'couleur', 'favori')
        }),
        ('Métadonnées', {
            'fields': ('cree_le', 'modifie_le'),
            'classes': ('collapse',),
        }),
    )


@admin.register(HistoriqueConsultation)
class HistoriqueConsultationAdmin(admin.ModelAdmin):
    list_display = ('fiche', 'date_consultation', 'titre', 'duree_minutes', 'cree_le')
    list_filter = ('date_consultation', 'cree_le')
    search_fields = ('titre', 'notes_generales', 'sujet_sentimental',
                     'sujet_professionnel', 'sujet_financier')
    date_hierarchy = 'date_consultation'
    list_per_page = 30


@admin.register(RendezVous)
class RendezVousAdmin(admin.ModelAdmin):
    list_display = ('fiche', 'date_rdv', 'heure_rdv', 'statut', 'sujet_prevu_court')
    list_filter = ('statut', 'date_rdv')
    search_fields = ('fiche__nom', 'fiche__prenom', 'sujet_prevu', 'notes')
    date_hierarchy = 'date_rdv'
    list_editable = ('statut',)
    list_per_page = 30
    
    @admin.display(description="Sujet")
    def sujet_prevu_court(self, obj):
        if obj.sujet_prevu:
            return obj.sujet_prevu[:50] + ('...' if len(obj.sujet_prevu) > 50 else '')
        return '—'