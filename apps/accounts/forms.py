from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User


class UserCreateForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'role', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={
                'placeholder': "Nom d'utilisateur",
                'autocomplete': 'off'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Labels personnalisés
        self.fields['username'].label = "Nom d'utilisateur"
        self.fields['role'].label = "Rôle"
        self.fields['password1'].label = "Mot de passe"
        self.fields['password2'].label = "Confirmer le mot de passe"
        
        # Placeholders
        self.fields['password1'].widget.attrs.update({
            'placeholder': 'Mot de passe',
            'autocomplete': 'new-password'
        })
        self.fields['password2'].widget.attrs.update({
            'placeholder': 'Confirmer le mot de passe',
            'autocomplete': 'new-password'
        })
        
        for field in self.fields.values():
            field.widget.attrs.setdefault(
                'class',
                'w-full px-4 py-2.5 rounded-xl border border-slate-200 '
                'focus:border-purple-400 focus:ring-2 focus:ring-purple-200 '
                'outline-none transition'
            )


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'role', 'bio', 'actif']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['username'].label = "Nom d'utilisateur"
        self.fields['role'].label = "Rôle"
        self.fields['bio'].label = "Bio / Notes (optionnel)"
        self.fields['actif'].label = "Compte actif"
        
        for field in self.fields.values():
            field.widget.attrs.setdefault(
                'class',
                'w-full px-4 py-2.5 rounded-xl border border-slate-200 '
                'focus:border-purple-400 focus:ring-2 focus:ring-purple-200 '
                'outline-none transition'
            )