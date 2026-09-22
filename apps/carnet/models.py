from django.db import models
from django.conf import settings
from datetime import date


# ============================================================
# SIGNE ASTROLOGIQUE AUTOMATIQUE
# ============================================================

def calculer_signe_astrologique(date_naissance):
    """Retourne le signe astrologique depuis une date de naissance."""
    if not date_naissance:
        return ''
    
    jour = date_naissance.day
    mois = date_naissance.month
    
    # (mois_début, jour_début, signe)
    # Chaque signe commence à cette date
    signes = [
        (1, 20, 'Verseau'),      # 20 jan → 18 fév
        (2, 19, 'Poissons'),     # 19 fév → 20 mar
        (3, 21, 'Bélier'),       # 21 mar → 19 avr
        (4, 20, 'Taureau'),      # 20 avr → 20 mai
        (5, 21, 'Gémeaux'),      # 21 mai → 20 jun
        (6, 21, 'Cancer'),       # 21 jun → 22 jul
        (7, 23, 'Lion'),         # 23 jul → 22 aoû
        (8, 23, 'Vierge'),       # 23 aoû → 22 sep
        (9, 23, 'Balance'),      # 23 sep → 22 oct
        (10, 23, 'Scorpion'),    # 23 oct → 21 nov
        (11, 22, 'Sagittaire'),  # 22 nov → 21 déc
        (12, 22, 'Capricorne'),  # 22 déc → 19 jan
    ]
    
    # On parcourt à l'envers : le dernier signe dont la date de début <= notre date
    for mois_debut, jour_debut, signe in reversed(signes):
        if mois > mois_debut or (mois == mois_debut and jour >= jour_debut):
            return signe
    
    # Cas particulier : date avant le 20 janvier → Capricorne
    return 'Capricorne'


# ============================================================
# NUMÉROLOGIE
# ============================================================

def reduire_nombre(n):
    """Réduit un nombre à 1-9 sauf 11, 22, 33 (maîtres)."""
    while n > 9 and n not in (11, 22, 33):
        n = sum(int(c) for c in str(n))
    return n


def calculer_chemin_de_vie(date_naissance):
    """Chemin de vie : somme de tous les chiffres de la date."""
    if not date_naissance:
        return None
    total = sum(int(c) for c in date_naissance.strftime('%d%m%Y'))
    return reduire_nombre(total)


def calculer_annee_personnelle(date_naissance):
    """Année personnelle : jour + mois de naissance + année actuelle."""
    if not date_naissance:
        return None
    annee_actuelle = date.today().year
    total = (date_naissance.day + date_naissance.month + 
             sum(int(c) for c in str(annee_actuelle)))
    return reduire_nombre(total)


def calculer_chiffre_cle(date_naissance):
    """Chiffre clé : jour de naissance réduit."""
    if not date_naissance:
        return None
    return reduire_nombre(date_naissance.day)


# ============================================================
# MODÈLES
# ============================================================

class FicheClient(models.Model):
    """Fiche personnelle d'un voyant sur un client"""
    
    SEXE_CHOICES = [
        ('M', 'Masculin'),
        ('F', 'Féminin'),
        ('A', 'Autre'),
    ]
    
    voyant = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='fiches'
    )
    
    # Identité
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100, blank=True)
    telephone = models.CharField(max_length=30, blank=True)
    email = models.EmailField(blank=True)
    sexe = models.CharField(max_length=1, choices=SEXE_CHOICES, blank=True)
    
    # Naissance
    date_naissance = models.DateField(null=True, blank=True)
    lieu_naissance = models.CharField(max_length=200, blank=True)
    signe_astrologique = models.CharField(max_length=50, blank=True)
    
    # Numérologie (calculés automatiquement, mais stockés)
    chemin_de_vie = models.PositiveSmallIntegerField(null=True, blank=True)
    annee_personnelle = models.PositiveSmallIntegerField(null=True, blank=True)
    chiffre_cle = models.PositiveSmallIntegerField(null=True, blank=True)
    
    # Vie personnelle
    situation_familiale = models.CharField(max_length=100, blank=True)
    profession = models.CharField(max_length=150, blank=True)
    nombre_enfants = models.PositiveSmallIntegerField(null=True, blank=True)
    
    # Description libre
    description_generale = models.TextField(
        blank=True,
        help_text="Qui est ce client ? Son histoire, son caractère..."
    )
    
    # Forfait
    forfait = models.CharField(
        max_length=200, blank=True,
        help_text="Ex: 'Forfait Premium 50€', 'Pack découverte', etc."
    )
    forfait_montant = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True,
        help_text="Montant payé par le client (optionnel)"
    )
    forfait_notes = models.CharField(max_length=200, blank=True)
    
    # Organisation
    tags = models.JSONField(default=list, blank=True)
    couleur = models.CharField(max_length=7, default='#7c3aed')
    favori = models.BooleanField(default=False)
    
    # Métadonnées
    cree_le = models.DateTimeField(auto_now_add=True)
    modifie_le = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-favori', '-modifie_le']
        indexes = [
            models.Index(fields=['voyant', '-modifie_le']),
            models.Index(fields=['voyant', 'nom']),
        ]
    
    def __str__(self):
        return self.nom_complet
    
    @property
    def nom_complet(self):
        return f"{self.prenom} {self.nom}".strip()
    
    @property
    def age(self):
        if not self.date_naissance:
            return None
        today = date.today()
        return today.year - self.date_naissance.year - (
            (today.month, today.day) < (self.date_naissance.month, self.date_naissance.day)
        )
    
    @property
    def anniversaire_dans(self):
        """Nombre de jours avant l'anniversaire"""
        if not self.date_naissance:
            return None
        today = date.today()
        prochain = self.date_naissance.replace(year=today.year)
        if prochain < today:
            prochain = prochain.replace(year=today.year + 1)
        return (prochain - today).days
    
    def save(self, *args, **kwargs):
        # Calcul automatique du signe astrologique
        if self.date_naissance:
            self.signe_astrologique = calculer_signe_astrologique(self.date_naissance)
            self.chemin_de_vie = calculer_chemin_de_vie(self.date_naissance)
            self.annee_personnelle = calculer_annee_personnelle(self.date_naissance)
            self.chiffre_cle = calculer_chiffre_cle(self.date_naissance)
        super().save(*args, **kwargs)
    
    @property
    def prochain_rdv(self):
        """Retourne le prochain RDV futur"""
        return self.rendezvous.filter(
            date_rdv__gte=date.today(),
            statut='planifie'
        ).order_by('date_rdv', 'heure_rdv').first()


class HistoriqueConsultation(models.Model):
    """Historique d'une consultation avec un client - peut contenir plusieurs sujets"""
    
    fiche = models.ForeignKey(
        FicheClient,
        on_delete=models.CASCADE,
        related_name='historiques'
    )
    
    # Date de la consultation
    date_consultation = models.DateField(default=date.today)
    
    # Titre automatique ou libre
    titre = models.CharField(
        max_length=200, blank=True,
        help_text="Ex: '1ère consultation', '2ème consultation', laissez vide pour auto"
    )
    
    # Notes libres générales
    notes_generales = models.TextField(
        blank=True,
        help_text="Résumé général de la consultation"
    )
    
    # Les 3 modules de sujets
    sujet_sentimental = models.TextField(
        blank=True,
        help_text="Ce qu'on a abordé côté sentiment/amour"
    )
    sujet_professionnel = models.TextField(
        blank=True,
        help_text="Ce qu'on a abordé côté travail/carrière"
    )
    sujet_financier = models.TextField(
        blank=True,
        help_text="Ce qu'on a abordé côté argent/finances"
    )
    
    # Durée
    duree_minutes = models.PositiveIntegerField(null=True, blank=True)
    
    cree_le = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-date_consultation', '-cree_le']
    
    def __str__(self):
        return f"{self.titre_auto} - {self.fiche.nom_complet}"
    
    @property
    def titre_auto(self):
        if self.titre:
            return self.titre
        # Compte le nombre d'historiques avant celui-ci
        count = HistoriqueConsultation.objects.filter(
            fiche=self.fiche,
            date_consultation__lt=self.date_consultation
        ).count()
        return f"{count + 1}ère consultation" if count == 0 else f"{count + 1}ème consultation"
    
    @property
    def a_des_sujets(self):
        return bool(self.sujet_sentimental or self.sujet_professionnel or self.sujet_financier)


class RendezVous(models.Model):
    """Rendez-vous planifié avec un client"""
    
    STATUT_CHOICES = [
        ('planifie', 'Planifié'),
        ('confirme', 'Confirmé'),
        ('termine', 'Terminé'),
        ('annule', 'Annulé'),
        ('reporte', 'Reporté'),
    ]
    
    MODE_CHOICES = [
        ('telephone', 'Téléphone'),
        ('chat', 'Chat'),
        ('visio', 'Visioconférence'),
        ('presentiel', 'Présentiel'),
    ]
    
    fiche = models.ForeignKey(
        FicheClient,
        on_delete=models.CASCADE,
        related_name='rendezvous'
    )
    date_rdv = models.DateField()
    heure_rdv = models.TimeField()
    duree_estimee = models.PositiveIntegerField(
        default=30,
        help_text="Durée en minutes"
    )
    mode = models.CharField(max_length=20, choices=MODE_CHOICES, default='telephone')
    sujet_prevu = models.TextField(
        blank=True,
        help_text="De quoi va-t-on parler ?"
    )
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='planifie')
    notes = models.TextField(blank=True)
    cree_le = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['date_rdv', 'heure_rdv']
    
    def __str__(self):
        return f"RDV {self.fiche.nom_complet} - {self.date_rdv} {self.heure_rdv}"
    
    @property
    def est_passe(self):
        from datetime import datetime
        return datetime.combine(self.date_rdv, self.heure_rdv) < datetime.now()
    
    @property
    def jours_restants(self):
        return (self.date_rdv - date.today()).days