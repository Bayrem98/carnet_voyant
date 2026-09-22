from django import forms
from .models import FicheClient, HistoriqueConsultation, RendezVous


class FicheClientForm(forms.ModelForm):
    """Formulaire de création/modification d'une fiche client."""
    
    class Meta:
        model = FicheClient
        fields = [
            # Identité
            'nom', 'sexe',
            # Naissance
            'date_naissance',
            # Forfait
            'forfait', 'forfait_montant',
            # Description
            'description_generale',
        ]
        widgets = {
            'date_naissance': forms.DateInput(attrs={'type': 'date'}),
            'description_generale': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Qui est ce client ? Son caractère, son histoire...'
            }),
            'forfait': forms.TextInput(attrs={
                'placeholder': "Ex: Forfait Premium 50€, Pack découverte..."
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Nom obligatoire
        self.fields['nom'].required = True
        self.fields['nom'].label = "Nom du client *"
        
        # Style uniforme
        for field in self.fields.values():
            field.widget.attrs.setdefault(
                'class',
                'w-full px-4 py-2.5 rounded-xl border border-slate-200 '
                'focus:border-purple-400 focus:ring-2 focus:ring-purple-200 '
                'outline-none transition'
            )


class HistoriqueConsultationForm(forms.ModelForm):
    class Meta:
        model = HistoriqueConsultation
        fields = [
            'date_consultation', 'titre', 'notes_generales',
            'sujet_sentimental', 'sujet_professionnel', 'sujet_financier',
            'duree_minutes',
        ]
        widgets = {
            'date_consultation': forms.DateInput(attrs={'type': 'date'}),
            'notes_generales': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Résumé général...'}),
            'sujet_sentimental': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Amour, sentiments, famille...'}),
            'sujet_professionnel': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Travail, carrière, projets...'}),
            'sujet_financier': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Argent, finances, investissements...'}),
            'titre': forms.TextInput(attrs={'placeholder': "Laissez vide pour '1ère consultation' automatique"}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.setdefault(
                'class',
                'w-full px-4 py-2.5 rounded-xl border border-slate-200 focus:border-purple-400 focus:ring-2 focus:ring-purple-200 outline-none transition'
            )


class RendezVousForm(forms.ModelForm):
    class Meta:
        model = RendezVous
        fields = [
            'date_rdv', 'heure_rdv', 'duree_estimee', 'mode',
            'sujet_prevu', 'statut', 'notes',
        ]
        widgets = {
            'date_rdv': forms.DateInput(attrs={'type': 'date'}),
            'heure_rdv': forms.TimeInput(attrs={'type': 'time'}),
            'sujet_prevu': forms.Textarea(attrs={'rows': 2, 'placeholder': 'De quoi allez-vous parler ?'}),
            'notes': forms.Textarea(attrs={'rows': 2}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.setdefault(
                'class',
                'w-full px-4 py-2.5 rounded-xl border border-slate-200 focus:border-purple-400 focus:ring-2 focus:ring-purple-200 outline-none transition'
            )