"""
Script pour charger/supprimer les données de test.

Usage :
    python seed_data.py           # Charge les données
    python seed_data.py --reset   # Supprime toutes les données de test
"""
import os
import sys
import django
from datetime import date, timedelta, time
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.accounts.models import User
from apps.carnet.models import FicheClient, HistoriqueConsultation, RendezVous


# ============================================================
# VOYANTS (username + password uniquement)
# ============================================================
VOYANTS = [
    {'username': 'marie', 'password': 'test1234'},
    {'username': 'sophie', 'password': 'test1234'},
    {'username': 'jean', 'password': 'test1234'},
]


# ============================================================
# CLIENTS
# ============================================================
CLIENTS = [
    {
        'nom': 'Youssef Alami',
        'sexe': 'M',
        'date_naissance': date(1985, 3, 15),
        'lieu_naissance': 'Casablanca',
        'situation_familiale': 'Marié',
        'profession': 'Ingénieur',
        'nombre_enfants': 2,
        'histoire': "Youssef est un homme posé qui consulte principalement pour des questions professionnelles. Il a traversé une période difficile après un licenciement, mais a su rebondir. Marié depuis 8 ans, père de 2 enfants. Il apprécie les consultations de suivi régulières.",
    },
    {
        'nom': 'Thomas Bernard',
        'sexe': 'M',
        'date_naissance': date(1978, 7, 22),
        'lieu_naissance': 'Paris',
        'situation_familiale': 'Divorcé',
        'profession': 'Avocat',
        'nombre_enfants': 1,
        'histoire': "Thomas est divorcé depuis 2 ans. Il consulte pour comprendre sa situation sentimentale compliquée et pour des questions autour de la garde de son enfant. Personnalité analytique, il pose beaucoup de questions précises.",
    },
    {
        'nom': 'Mehdi Trabelsi',
        'sexe': 'M',
        'date_naissance': date(1992, 11, 8),
        'lieu_naissance': 'Tunis',
        'situation_familiale': 'Célibataire',
        'profession': 'Développeur web',
        'nombre_enfants': 0,
        'histoire': "Mehdi est célibataire, un peu perdu dans sa vie amoureuse. Il cherche à comprendre pourquoi ses relations ne durent pas. Très ouvert d'esprit, réceptif aux conseils.",
    },
    {
        'nom': 'Lucas Moreau',
        'sexe': 'M',
        'date_naissance': date(1995, 5, 3),
        'lieu_naissance': 'Lyon',
        'situation_familiale': 'Célibataire',
        'profession': 'Étudiant en droit',
        'nombre_enfants': 0,
        'histoire': "Lucas est étudiant en fin de cursus. Il consulte pour son orientation professionnelle et ses examens à venir. Anxieux, il a besoin d'être rassuré.",
    },
    {
        'nom': 'Antoine Rousseau',
        'sexe': 'M',
        'date_naissance': date(1980, 9, 28),
        'lieu_naissance': 'Marseille',
        'situation_familiale': 'Marié',
        'profession': "Chef d'entreprise",
        'nombre_enfants': 3,
        'histoire': "Antoine dirige une PME. Il consulte régulièrement pour des décisions stratégiques et des questions financières. Homme de pouvoir, il cherche des confirmations plutôt que des conseils.",
    },
    {
        'nom': 'Pierre Lefevre',
        'sexe': 'M',
        'date_naissance': date(1968, 1, 12),
        'lieu_naissance': 'Bordeaux',
        'situation_familiale': 'Veuf',
        'profession': 'Retraité',
        'nombre_enfants': 2,
        'histoire': "Pierre a perdu son épouse il y a 3 ans. Il consulte pour faire son deuil et pour des questions spirituelles. Homme cultivé, il apprécie les consultations longues et profondes.",
    },
    {
        'nom': 'Salma El Fassi',
        'sexe': 'F',
        'date_naissance': date(1990, 8, 14),
        'lieu_naissance': 'Rabat',
        'situation_familiale': 'Mariée',
        'profession': 'Architecte',
        'nombre_enfants': 1,
        'histoire': "Salma est mariée et mère d'un enfant. Elle consulte pour des questions familiales et pour un projet de reconversion. Très émotive, elle vit ses consultations intensément.",
    },
    {
        'nom': 'Julie Petit',
        'sexe': 'F',
        'date_naissance': date(1987, 2, 7),
        'lieu_naissance': 'Paris',
        'situation_familiale': 'Célibataire',
        'profession': 'Enseignante',
        'nombre_enfants': 0,
        'histoire': "Julie est célibataire, en recherche de sens. Elle consulte pour sa vie amoureuse et pour des questions existentielles. Douce et sensible, elle a besoin de réconfort.",
    },
    {
        'nom': 'Camille Roux',
        'sexe': 'F',
        'date_naissance': date(1983, 6, 30),
        'lieu_naissance': 'Nice',
        'situation_familiale': 'Divorcée',
        'profession': 'Infirmière',
        'nombre_enfants': 2,
        'histoire': "Camille est divorcée et élève seule ses 2 enfants. Elle consulte pour des questions financières et professionnelles. Femme forte mais fatiguée, elle cherche des solutions concrètes.",
    },
    {
        'nom': 'Ines Hammami',
        'sexe': 'F',
        'date_naissance': date(1996, 10, 11),
        'lieu_naissance': 'Sfax',
        'situation_familiale': 'Célibataire',
        'profession': 'Étudiante en médecine',
        'nombre_enfants': 0,
        'histoire': "Ines est en fin d'études de médecine. Elle consulte pour son avenir professionnel et pour une histoire d'amour naissante. Sérieuse et appliquée, elle suit scrupuleusement les conseils.",
    },
    {
        'nom': 'Céline Fournier',
        'sexe': 'F',
        'date_naissance': date(1972, 5, 4),
        'lieu_naissance': 'Strasbourg',
        'situation_familiale': 'Mariée',
        'profession': 'Comptable',
        'nombre_enfants': 2,
        'histoire': "Céline est mariée depuis 20 ans. Elle consulte pour faire le point sur sa vie et pour un projet de voyage. Discrète, elle parle peu d'elle mais écoute beaucoup.",
    },
    {
        'nom': 'Élodie Girard',
        'sexe': 'F',
        'date_naissance': date(1985, 1, 20),
        'lieu_naissance': 'Lille',
        'situation_familiale': 'Mariée',
        'profession': 'Coiffeuse',
        'nombre_enfants': 1,
        'histoire': "Élodie a un salon de coiffure. Elle consulte pour des questions financières et pour une éventuelle expansion. Pragmatique, elle cherche des réponses claires.",
    },
    {
        'nom': 'Manon Mercier',
        'sexe': 'F',
        'date_naissance': date(1998, 11, 2),
        'lieu_naissance': 'Nantes',
        'situation_familiale': 'Célibataire',
        'profession': 'Serveuse',
        'nombre_enfants': 0,
        'histoire': "Manon est jeune et pleine de vie. Elle consulte pour ses histoires d'amour compliquées et pour son avenir. Sceptique au départ, elle devient vite convaincue.",
    },
    {
        'nom': 'Yasmine Ben Salah',
        'sexe': 'F',
        'date_naissance': date(1979, 3, 19),
        'lieu_naissance': 'Tunis',
        'situation_familiale': 'Mariée',
        'profession': 'Pharmacienne',
        'nombre_enfants': 3,
        'histoire': "Yasmine tient une pharmacie familiale. Elle consulte pour ses enfants et pour sa santé. Réservée, elle apprécie la discrétion et la bienveillance.",
    },
    {
        'nom': 'Amélie Laurent',
        'sexe': 'F',
        'date_naissance': date(1993, 7, 27),
        'lieu_naissance': 'Rennes',
        'situation_familiale': 'En couple',
        'profession': 'Graphiste freelance',
        'nombre_enfants': 0,
        'histoire': "Amélie est graphiste indépendante. Elle consulte pour son couple et pour ses projets professionnels. Créative, elle cherche de l'inspiration et de la clarté.",
    },
    {
        'nom': 'Elena Sanchez',
        'sexe': 'F',
        'date_naissance': date(1965, 9, 8),
        'lieu_naissance': 'Montpellier',
        'situation_familiale': 'Mariée',
        'profession': 'Retraitée',
        'nombre_enfants': 2,
        'histoire': "Elena est retraitée et profite de la vie. Elle consulte pour ses petits-enfants et pour des questions spirituelles. Sage et posée, elle aime partager.",
    },
    {
        'nom': 'Rim Bouhlel',
        'sexe': 'F',
        'date_naissance': date(1989, 12, 30),
        'lieu_naissance': 'Djerba',
        'situation_familiale': 'Mariée',
        'profession': 'Professeure',
        'nombre_enfants': 1,
        'histoire': "Rim enseigne au lycée. Elle consulte pour sa carrière et pour des questions familiales. Passionnée, elle aime comprendre les choses en profondeur.",
    },
    {
        'nom': 'Alex Taylor',
        'sexe': 'A',
        'date_naissance': date(1991, 4, 15),
        'lieu_naissance': 'Bruxelles',
        'situation_familiale': 'Célibataire',
        'profession': 'Artiste',
        'nombre_enfants': 0,
        'histoire': "Alex est artiste et vit de sa passion. Il/elle consulte pour des questions existentielles et pour son évolution créative. Ouvert(e) et curieux(se), iel apprécie les échanges profonds.",
    },
    {
        'nom': 'Ji-ho Kim',
        'sexe': 'A',
        'date_naissance': date(1994, 8, 22),
        'lieu_naissance': 'Séoul',
        'situation_familiale': 'En couple',
        'profession': 'Designer',
        'nombre_enfants': 0,
        'histoire': "Ji-ho est designer dans une agence internationale. Iel consulte pour son couple et pour un projet de déménagement à l'étranger. Réfléchi(e), iel pèse chaque mot.",
    },
]


# ============================================================
# NOTES POUR CONSULTATIONS
# ============================================================
NOTES_SENTIMENTAL = [
    "Période de doute sentimental. À rassurer sur son avenir amoureux.",
    "Rencontre importante à venir dans les prochains mois. Rester ouvert(e).",
    "Relation actuelle à consolider. Ne pas précipiter les choses.",
    "Amour secret non révélé. Situation à surveiller.",
    "Passé sentimental douloureux. Travail de guérison en cours.",
]

NOTES_PROFESSIONNEL = [
    "Changement professionnel favorable à venir. Préparer le terrain.",
    "Tension au travail avec un collègue. Rester diplomate.",
    "Opportunité à saisir d'ici 3 mois. Être prêt(e).",
    "Projet de reconversion à étudier sérieusement.",
    "Promotion possible si le travail continue dans cette voie.",
]

NOTES_FINANCIER = [
    "Période financière délicate mais temporaire.",
    "Investissement à envisager avec prudence.",
    "Entrée d'argent inattendue possible.",
    "Éviter les dépenses impulsives ce mois-ci.",
    "Situation financière stable, propice à l'épargne.",
]

NOTES_GENERALES = [
    "Consultation classique, le/la client(e) est reparti(e) apaisé(e).",
    "Séance intense avec beaucoup d'émotions.",
    "Très bonne énergie pendant la consultation.",
    "Consultation de suivi, vérification des prédictions passées.",
    "Le/la client(e) est venu(e) chercher des réponses précises.",
]


# ============================================================
# FONCTION CHARGEMENT
# ============================================================
def run():
    print("🚀 Chargement des données...\n")
    random.seed(42)
    
    # 1. Créer les voyants
    voyants_obj = []
    for v in VOYANTS:
        user, created = User.objects.get_or_create(
            username=v['username'],
            defaults={'role': 'voyant', 'actif': True}
        )
        if created:
            user.set_password(v['password'])
            user.save()
            print(f"✅ Voyant créé : {user.username} (mdp: {v['password']})")
        else:
            print(f"↩️  Voyant existant : {user.username}")
        voyants_obj.append(user)
    
    # 2. Créer les fiches clients
    print(f"\n📋 Création des fiches clients...\n")
    fiches_creees = 0
    
    for i, c in enumerate(CLIENTS):
        voyant = voyants_obj[i % len(voyants_obj)]
        
        if FicheClient.objects.filter(voyant=voyant, nom=c['nom']).exists():
            print(f"↩️  Fiche existante : {c['nom']}")
            continue
        
        # Choisir un forfait aléatoire
        forfait = random.choice(['140', '280', '400', '700', '900', '1300'])
        total_minutes = {'140': 30, '280': 60, '400': 90,
                        '700': 150, '900': 180, '1300': 300}[forfait]
        minutes_utilisees = random.randint(int(total_minutes * 0.3), int(total_minutes * 0.9))
        
        # Créer la fiche
        fiche = FicheClient.objects.create(
            voyant=voyant,
            nom=c['nom'],
            sexe=c['sexe'],
            date_naissance=c['date_naissance'],
            lieu_naissance=c['lieu_naissance'],
            situation_familiale=c['situation_familiale'],
            profession=c['profession'],
            nombre_enfants=c['nombre_enfants'],
            description_generale=c['histoire'],
            forfait=forfait,
            forfait_minutes_utilisees=minutes_utilisees,
            favori=random.random() < 0.25,
        )
        fiches_creees += 1
        print(f"✅ {fiche.nom_complet} → {voyant.username} (Forfait {forfait}€)")
        
        # 3. Ajouter 1 à 3 consultations
        nb_consult = random.randint(1, 3)
        for j in range(nb_consult):
            jours = random.randint(10, 150)
            date_cons = date.today() - timedelta(days=jours)
            
            HistoriqueConsultation.objects.create(
                fiche=fiche,
                date_consultation=date_cons,
                notes_generales=random.choice(NOTES_GENERALES),
                sujet_sentimental=random.choice(NOTES_SENTIMENTAL) if random.random() < 0.8 else '',
                sujet_professionnel=random.choice(NOTES_PROFESSIONNEL) if random.random() < 0.7 else '',
                sujet_financier=random.choice(NOTES_FINANCIER) if random.random() < 0.6 else '',
                duree_minutes=random.choice([20, 30, 45, 60]),
            )
        
        # 4. Ajouter 1 à 2 RDV
        nb_rdv = random.randint(1, 2)
        for k in range(nb_rdv):
            jours = random.randint(-20, 30)
            date_rdv = date.today() + timedelta(days=jours)
            heure_rdv = time(random.randint(9, 18), random.choice([0, 15, 30, 45]))
            
            if jours < 0:
                statut = random.choice(['termine', 'annule'])
            else:
                statut = random.choice(['planifie', 'confirme'])
            
            RendezVous.objects.create(
                fiche=fiche,
                date_rdv=date_rdv,
                heure_rdv=heure_rdv,
                statut=statut,
                sujet_prevu=random.choice([
                    "Faire le point sur la situation",
                    "Suite de la consultation précédente",
                    "Question sur un projet important",
                    "Tirage complet",
                ]),
            )
    
    # 5. Récap
    print(f"\n{'='*60}")
    print(f"📊 RÉCAPITULATIF")
    print(f"{'='*60}")
    print(f"Voyants créés         : {User.objects.filter(role='voyant').count()}")
    print(f"Fiches clients        : {FicheClient.objects.count()}")
    print(f"Consultations         : {HistoriqueConsultation.objects.count()}")
    print(f"RDV                   : {RendezVous.objects.count()}")
    print(f"\n🔑 Connexion voyant (mot de passe : test1234)")
    for v in VOYANTS:
        print(f"   - {v['username']}")
    print(f"\n💡 Pour tout supprimer : python seed_data.py --reset\n")


# ============================================================
# FONCTION RESET
# ============================================================
def reset():
    print("⚠️  Suppression de toutes les données de test...\n")
    
    n_rdv = RendezVous.objects.count()
    n_hist = HistoriqueConsultation.objects.count()
    n_fiches = FicheClient.objects.count()
    n_voyants = User.objects.filter(role='voyant').count()
    
    RendezVous.objects.all().delete()
    HistoriqueConsultation.objects.all().delete()
    FicheClient.objects.all().delete()
    User.objects.filter(role='voyant').delete()
    
    print(f"✅ {n_voyants} voyant(s) supprimé(s)")
    print(f"✅ {n_fiches} fiche(s) supprimée(s)")
    print(f"✅ {n_hist} consultation(s) supprimée(s)")
    print(f"✅ {n_rdv} RDV supprimé(s)")
    print("\n🎯 Les admins et responsables sont conservés.")


# ============================================================
# POINT D'ENTRÉE
# ============================================================
if __name__ == '__main__':
    if '--reset' in sys.argv:
        reset()
    else:
        run()