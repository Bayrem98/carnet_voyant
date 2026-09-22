from django.db import models
from django.conf import settings
from datetime import date


# ============================================================
# SIGNE ASTROLOGIQUE
# ============================================================

def calculer_signe_astrologique(date_naissance):
    """Retourne le signe astrologique depuis une date de naissance."""
    if not date_naissance:
        return ''
    
    jour = date_naissance.day
    mois = date_naissance.month
    
    signes = [
        (1, 20, 'Verseau'),
        (2, 19, 'Poissons'),
        (3, 21, 'Bélier'),
        (4, 20, 'Taureau'),
        (5, 21, 'Gémeaux'),
        (6, 21, 'Cancer'),
        (7, 23, 'Lion'),
        (8, 23, 'Vierge'),
        (9, 23, 'Balance'),
        (10, 23, 'Scorpion'),
        (11, 22, 'Sagittaire'),
        (12, 22, 'Capricorne'),
    ]
    
    for mois_debut, jour_debut, signe in reversed(signes):
        if mois > mois_debut or (mois == mois_debut and jour >= jour_debut):
            return signe
    
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
    if not date_naissance:
        return None
    total = sum(int(c) for c in date_naissance.strftime('%d%m%Y'))
    return reduire_nombre(total)


def calculer_annee_personnelle(date_naissance):
    if not date_naissance:
        return None
    annee_actuelle = date.today().year
    total = (date_naissance.day + date_naissance.month + 
             sum(int(c) for c in str(annee_actuelle)))
    return reduire_nombre(total)


def calculer_chiffre_cle(date_naissance):
    if not date_naissance:
        return None
    return reduire_nombre(date_naissance.day)


# ============================================================
# FORFAITS (avec minutes associées)
# ============================================================

FORFAITS = [
    ('140', 'Forfait 140€ - 30 minutes', 140, 30),
    ('280', 'Forfait 280€ - 60 minutes', 280, 60),
    ('400', 'Forfait 400€ - 90 minutes', 400, 90),
    ('700', 'Forfait 700€ - 150 minutes', 700, 150),
    ('900', 'Forfait 900€ - 180 minutes', 900, 180),
    ('1300', 'Forfait 1300€ - 300 minutes', 1300, 300),
]

FORFAIT_CHOICES = [(code, label) for code, label, prix, minutes in FORFAITS]
FORFAIT_MONTANTS = {code: prix for code, label, prix, minutes in FORFAITS}
FORFAIT_MINUTES = {code: minutes for code, label, prix, minutes in FORFAITS}


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
    
    # Numérologie (calculée)
    chemin_de_vie = models.PositiveSmallIntegerField(null=True, blank=True)
    annee_personnelle = models.PositiveSmallIntegerField(null=True, blank=True)
    chiffre_cle = models.PositiveSmallIntegerField(null=True, blank=True)
    
    # Vie personnelle
    situation_familiale = models.CharField(max_length=100, blank=True)
    profession = models.CharField(max_length=150, blank=True)
    nombre_enfants = models.PositiveSmallIntegerField(null=True, blank=True)
    
    # Description
    description_generale = models.TextField(
        blank=True,
        help_text="Qui est ce client ? Son histoire, son caractère..."
    )
    
    # Forfait
    forfait = models.CharField(
        max_length=20, choices=FORFAIT_CHOICES, blank=True,
        help_text="Forfait souscrit par le client"
    )
    forfait_minutes_utilisees = models.PositiveIntegerField(
        default=0,
        help_text="Nombre de minutes déjà consommées"
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
        return f"{self.prenom} {self.nom}".strip() or self.nom
    
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
        if not self.date_naissance:
            return None
        today = date.today()
        prochain = self.date_naissance.replace(year=today.year)
        if prochain < today:
            prochain = prochain.replace(year=today.year + 1)
        return (prochain - today).days
    
    @property
    def forfait_prix(self):
        """Retourne le prix du forfait en euros."""
        if not self.forfait:
            return None
        return FORFAIT_MONTANTS.get(self.forfait)
    
    @property
    def forfait_minutes_total(self):
        """Retourne le nombre total de minutes du forfait."""
        if not self.forfait:
            return None
        return FORFAIT_MINUTES.get(self.forfait)
    
    @property
    def forfait_minutes_restantes(self):
        """Retourne le nombre de minutes restantes."""
        if not self.forfait:
            return None
        total = self.forfait_minutes_total or 0
        return max(0, total - self.forfait_minutes_utilisees)
    
    @property
    def forfait_pourcentage_utilise(self):
        """Pourcentage du forfait utilisé."""
        if not self.forfait or not self.forfait_minutes_total:
            return 0
        return min(100, round((self.forfait_minutes_utilisees / self.forfait_minutes_total) * 100))
    
    @property
    def forfait_label(self):
        """Retourne le label complet du forfait."""
        if not self.forfait:
            return ''
        for code, label, prix, minutes in FORFAITS:
            if code == self.forfait:
                return label
        return self.forfait
    
    def save(self, *args, **kwargs):
        if self.date_naissance:
            self.signe_astrologique = calculer_signe_astrologique(self.date_naissance)
            self.chemin_de_vie = calculer_chemin_de_vie(self.date_naissance)
            self.annee_personnelle = calculer_annee_personnelle(self.date_naissance)
            self.chiffre_cle = calculer_chiffre_cle(self.date_naissance)
        super().save(*args, **kwargs)
    
    @property
    def prochain_rdv(self):
        return self.rendezvous.filter(
            date_rdv__gte=date.today(),
            statut__in=['planifie', 'confirme']
        ).order_by('date_rdv', 'heure_rdv').first()


class HistoriqueConsultation(models.Model):
    """Historique d'une consultation avec un client"""
    
    fiche = models.ForeignKey(
        FicheClient,
        on_delete=models.CASCADE,
        related_name='historiques'
    )
    
    date_consultation = models.DateField(default=date.today)
    titre = models.CharField(max_length=200, blank=True)
    notes_generales = models.TextField(blank=True)
    
    # 3 modules de sujets
    sujet_sentimental = models.TextField(blank=True)
    sujet_professionnel = models.TextField(blank=True)
    sujet_financier = models.TextField(blank=True)
    
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
        ('reporte', 'Reporté'),
        ('annule', 'Annulé'),
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
    duree_estimee = models.PositiveIntegerField(default=30)
    mode = models.CharField(max_length=20, choices=MODE_CHOICES, default='telephone')
    sujet_prevu = models.TextField(blank=True)
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
    def peut_changer_statut(self):
        """Peut-on changer le statut ? Oui si le RDV est passé et n'est pas déjà terminé/annulé."""
        return self.est_passe and self.statut not in ['termine', 'annule', 'reporte']
    
    @property
    def jours_restants(self):
        return (self.date_rdv - date.today()).days