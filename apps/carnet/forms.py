from django import forms
from .models import FicheClient, HistoriqueConsultation, RendezVous


class FicheClientForm(forms.ModelForm):
    """Formulaire de création/modification d'une fiche client."""
    
    # ✅ Forcer le format ISO pour la date (compatible <input type="date">)
    date_naissance = forms.DateField(
        required=False,
        widget=forms.DateInput(
            attrs={'type': 'date'},
            format='%Y-%m-%d'  # ← Format HTML5
        ),
        input_formats=['%Y-%m-%d', '%d/%m/%Y', '%d-%m-%Y'],  # ← Accepte plusieurs formats
    )
    
    class Meta:
        model = FicheClient
        fields = [
            'nom', 'sexe',
            'date_naissance', 'lieu_naissance',
            'situation_familiale', 'profession', 'nombre_enfants',
            'forfait', 'forfait_minutes_utilisees',
            'description_generale',
        ]
        widgets = {
            'description_generale': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Qui est ce client ? Son caractère, son histoire...'
            }),
            'forfait': forms.Select(),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['nom'].required = True
        self.fields['nom'].label = "Nom du client *"
        
        # ✅ S'assurer que la date initiale est bien au format ISO
        if self.instance and self.instance.pk and self.instance.date_naissance:
            self.initial['date_naissance'] = self.instance.date_naissance.strftime('%Y-%m-%d')
        
        for field in self.fields.values():
            field.widget.attrs.setdefault(
                'class',
                'w-full px-4 py-2.5 rounded-xl border border-slate-200 '
                'focus:border-purple-400 focus:ring-2 focus:ring-purple-200 '
                'outline-none transition'
            )


class HistoriqueConsultationForm(forms.ModelForm):
    # ✅ Forcer le format ISO
    date_consultation = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
        input_formats=['%Y-%m-%d', '%d/%m/%Y'],
    )
    
    class Meta:
        model = HistoriqueConsultation
        fields = [
            'date_consultation', 'titre', 'notes_generales',
            'sujet_sentimental', 'sujet_professionnel', 'sujet_financier',
            'duree_minutes',
        ]
        widgets = {
            'notes_generales': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Résumé général...'}),
            'sujet_sentimental': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Amour, sentiments, famille...'}),
            'sujet_professionnel': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Travail, carrière, projets...'}),
            'sujet_financier': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Argent, finances, investissements...'}),
            'titre': forms.TextInput(attrs={'placeholder': "Laissez vide pour numérotation auto"}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # ✅ Forcer le format initial
        if self.instance and self.instance.pk and self.instance.date_consultation:
            self.initial['date_consultation'] = self.instance.date_consultation.strftime('%Y-%m-%d')
        
        for field in self.fields.values():
            field.widget.attrs.setdefault(
                'class',
                'w-full px-4 py-2.5 rounded-xl border border-slate-200 '
                'focus:border-purple-400 focus:ring-2 focus:ring-purple-200 '
                'outline-none transition'
            )


class RendezVousForm(forms.ModelForm):
    # ✅ Forcer le format ISO pour les dates
    date_rdv = forms.DateField(
        required=True,
        widget=forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
        input_formats=['%Y-%m-%d', '%d/%m/%Y'],
    )
    heure_rdv = forms.TimeField(
        required=True,
        widget=forms.TimeInput(attrs={'type': 'time'}, format='%H:%M'),
        input_formats=['%H:%M', '%H:%M:%S'],
    )
    
    class Meta:
        model = RendezVous
        fields = ['date_rdv', 'heure_rdv', 'statut', 'sujet_prevu']
        widgets = {
            'sujet_prevu': forms.Textarea(attrs={
                'rows': 2,
                'placeholder': 'De quoi allez-vous parler ?'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # ✅ Forcer le format initial
        if self.instance and self.instance.pk:
            if self.instance.date_rdv:
                self.initial['date_rdv'] = self.instance.date_rdv.strftime('%Y-%m-%d')
            if self.instance.heure_rdv:
                self.initial['heure_rdv'] = self.instance.heure_rdv.strftime('%H:%M')
        
        for field in self.fields.values():
            field.widget.attrs.setdefault(
                'class',
                'w-full px-4 py-2.5 rounded-xl border border-slate-200 '
                'focus:border-purple-400 focus:ring-2 focus:ring-purple-200 '
                'outline-none transition'
            )


class RendezVousStatutForm(forms.ModelForm):
    """Formulaire minimal pour changer juste le statut d'un RDV"""
    class Meta:
        model = RendezVous
        fields = ['statut', 'notes']
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Notes sur ce RDV...'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Limiter les choix aux statuts post-RDV
        self.fields['statut'].choices = [
            ('termine', 'Terminé'),
            ('reporte', 'Reporté'),
            ('annule', 'Annulé'),
        ]
        for field in self.fields.values():
            field.widget.attrs.setdefault(
                'class',
                'w-full px-4 py-2.5 rounded-xl border border-slate-200 '
                'focus:border-purple-400 focus:ring-2 focus:ring-purple-200 '
                'outline-none transition'
            )

class ReporterRdvForm(forms.Form):
    """Formulaire pour reporter un RDV (nouvelle date + heure)."""
    
    nouvelle_date = forms.DateField(
        label="Nouvelle date",
        widget=forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
        input_formats=['%Y-%m-%d', '%d/%m/%Y'],
        required=True,
    )
    nouvelle_heure = forms.TimeField(
        label="Nouvelle heure",
        widget=forms.TimeInput(attrs={'type': 'time'}, format='%H:%M'),
        input_formats=['%H:%M', '%H:%M:%S'],
        required=True,
    )
    raison = forms.CharField(
        label="Raison du report (optionnel)",
        widget=forms.Textarea(attrs={
            'rows': 3,
            'placeholder': 'Ex : Client malade, empêchement, à sa demande...'
        }),
        required=False,
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.setdefault(
                'class',
                'w-full px-4 py-2.5 rounded-xl border border-slate-200 '
                'focus:border-purple-400 focus:ring-2 focus:ring-purple-200 '
                'outline-none transition'
            )