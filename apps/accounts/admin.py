from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'nom_complet', 'role', 'actif', 'is_superuser', 'date_joined')
    list_filter = ('role', 'actif', 'is_superuser', 'is_staff', 'date_joined')
    search_fields = ('username', 'first_name', 'last_name', 'email')
    ordering = ('-date_joined',)
    list_editable = ('role', 'actif')
    
    fieldsets = (
        ('Identifiants', {
            'fields': ('username', 'password')
        }),
        ('Informations personnelles', {
            'fields': ('first_name', 'last_name', 'email', 'telephone_pro', 'avatar', 'bio')
        }),
        ('Rôle & Permissions', {
            'fields': ('role', 'actif', 'statut', 'specialites',
                      'is_active', 'is_staff', 'is_superuser',
                      'groups', 'user_permissions')
        }),
        ('Dates importantes', {
            'fields': ('last_login', 'date_joined'),
            'classes': ('collapse',),
        }),
    )
    
    add_fieldsets = (
        ('Créer un utilisateur', {
            'classes': ('wide',),
            'fields': ('username', 'role', 'password1', 'password2', 'actif'),
        }),
    )
    
    # Champs en lecture seule (non modifiables)
    readonly_fields = ('last_login', 'date_joined')


# Personnaliser le titre de l'admin
admin.site.site_header = "Carnet du Voyant — Administration"
admin.site.site_title = "Admin Carnet"
admin.site.index_title = "Panneau d'administration"