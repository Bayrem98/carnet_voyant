from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User


class UserCreateForm(UserCreationForm):
    class Meta:
        model = User
        fields = [
            'username', 'first_name', 'last_name', 'email',
            'role', 'telephone_pro', 'password1', 'password2',
        ]
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': "Nom d'utilisateur"}),
            'first_name': forms.TextInput(attrs={'placeholder': 'Prénom'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Nom'}),
            'email': forms.EmailInput(attrs={'placeholder': 'email@exemple.com'}),
            'telephone_pro': forms.TextInput(attrs={'placeholder': '06 12 34 56 78'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
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
        fields = [
            'username', 'first_name', 'last_name', 'email',
            'role', 'telephone_pro', 'bio', 'actif',
        ]
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.setdefault(
                'class',
                'w-full px-4 py-2.5 rounded-xl border border-slate-200 '
                'focus:border-purple-400 focus:ring-2 focus:ring-purple-200 '
                'outline-none transition'
            )