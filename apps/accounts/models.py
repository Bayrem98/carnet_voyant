from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLE_CHOICES = [
        ('voyant', 'Voyant'),
        ('responsable', 'Responsable'),
    ]
    
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='voyant')
    telephone_pro = models.CharField(max_length=30, blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    bio = models.TextField(blank=True, help_text="Présentation du voyant")
    
    # Pour les voyants
    specialites = models.JSONField(default=list, blank=True)  # ['tarot', 'astro']
    statut = models.CharField(
        max_length=20,
        choices=[
            ('disponible', 'Disponible'),
            ('en_consultation', 'En consultation'),
            ('pause', 'En pause'),
            ('hors_ligne', 'Hors ligne'),
        ],
        default='hors_ligne'
    )
    
    def is_voyant(self):
        return self.role == 'voyant'
    
    def is_responsable(self):
        return self.role == 'responsable'
    
    def __str__(self):
        return f"{self.get_full_name() or self.username}"