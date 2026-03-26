"""
Script de données de démonstration — Dr. Soumahoro Souleymane
Exécuter avec : python manage.py shell < seed_data.py
"""
import os
import django
import sys

# Configurer Django si lancé directement
if __name__ == '__main__':
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'website_ss.settings')
    django.setup()

from django.utils.text import slugify
from website.models import Actualite, NewsletterAbonne, MessageContact
from datetime import date

print("🌱 Insertion des données de démonstration...")

# ─── ACTUALITÉS ───────────────────────────────────
articles = [
    {
        "titre": "Participation à la Commission des Affaires Économiques et Financières",
        "extrait": "Le Député Dr. Soumahoro Souleymane a pris part à la réunion de la Commission des Affaires Économiques et Financières (CAEF) à l'Assemblée Nationale de Côte d'Ivoire.",
        "contenu": """Jeudi 12 mars 2026, le Dr. Soumahoro Souleymane, Député élu de la circonscription de Daleu, Danané, Gbon-Houyé, Kouan-Houlé et Seileu, a activement participé aux travaux de la Commission des Affaires Économiques et Financières (CAEF) à l'Assemblée Nationale.

Cette réunion a été l'occasion d'examiner plusieurs projets de loi relatifs au développement économique et à la fiscalité locale. Le Député a particulièrement insisté sur l'importance d'allouer des ressources supplémentaires aux circonscriptions rurales de l'Ouest de la Côte d'Ivoire.

Les discussions ont également porté sur les mécanismes de contrôle budgétaire et la transparence dans la gestion des fonds publics. Le Dr. Soumahoro a présenté plusieurs amendements visant à renforcer les investissements dans les infrastructures de sa circonscription.

La prochaine réunion de la CAEF est prévue pour fin mars 2026.""",
        "categorie": "assemblee",
        "date_publication": date(2026, 3, 12),
        "en_vedette": True,
        "publie": True,
    },
    {
        "titre": "Visite de courtoisie à l'occasion de l'Aïd El-Fitr à Danané",
        "extrait": "À l'occasion de la fête de l'Aïd El-Fitr, le Député s'est rendu à Danané où il a effectué une visite de courtoisie auprès des autorités locales et des responsables religieux.",
        "contenu": """À l'occasion de la célébration de l'Aïd El-Fitr 2026, le Dr. Soumahoro Souleymane, Député de la circonscription de Danané, a effectué une tournée de visites de courtoisie à travers sa circonscription.

Ces visites ont constitué un moment privilégié d'échanges avec les autorités locales, les chefs de communauté et les responsables religieux. Le Député est revenu sur les temps forts des premiers mois de son mandat et a présenté les projets en cours pour le développement de la région.

Les rencontres ont également permis d'écouter les préoccupations des populations locales, notamment en matière d'accès aux services de base, d'infrastructures routières et de développement agricole.

Le Député a réaffirmé son engagement à œuvrer pour le bien-être de tous les habitants de sa circonscription, dans un esprit de solidarité et d'unité.""",
        "categorie": "circonscription",
        "date_publication": date(2026, 3, 30),
        "en_vedette": False,
        "publie": True,
    },
    {
        "titre": "Première permanence à Danané : à l'écoute des citoyens",
        "extrait": "Le Député Dr. Soumahoro Souleymane a tenu sa première permanence officielle à Danané, recevant les habitants de sa circonscription pour écouter leurs préoccupations.",
        "contenu": """Le samedi 22 février 2026, le Dr. Soumahoro Souleymane a tenu sa première permanence parlementaire officielle dans sa circonscription de Danané.

Pendant plus de quatre heures, le Député a reçu des délégations de citoyens, d'associations locales, d'agriculteurs et d'entrepreneurs venus exposer leurs préoccupations et soumettre leurs projets. Cette rencontre directe avec la population a permis d'identifier les priorités urgentes : réhabilitation des routes rurales, accès à l'eau potable et renforcement du système éducatif.

Le Député a annoncé la mise en place d'un calendrier régulier de permanences dans les différentes communes de sa circonscription (Daleu, Danané, Gbon-Houyé, Kouan-Houlé et Seileu) pour maintenir ce lien de proximité avec les habitants.

Un registre de suivi des doléances a été mis en place pour assurer le traitement de chaque demande.""",
        "categorie": "circonscription",
        "date_publication": date(2026, 2, 22),
        "en_vedette": False,
        "publie": True,
    },
    {
        "titre": "Déclaration sur le projet de loi de finances rectificatif 2026",
        "extrait": "À l'occasion de l'examen du projet de loi de finances rectificatif, le Député a pris la parole en séance plénière pour défendre les intérêts des collectivités locales.",
        "contenu": """Lors de la séance plénière du 5 mars 2026 à l'Assemblée Nationale de Côte d'Ivoire, le Dr. Soumahoro Souleymane est intervenu dans le cadre de l'examen du projet de loi de finances rectificatif pour l'exercice 2026.

Dans son intervention, le Député a mis en lumière les disparités de financement entre les zones urbaines et les zones rurales, plaidant pour une révision des critères d'allocation des dotations de l'État aux collectivités locales.

Il a notamment proposé l'introduction d'un coefficient multiplicateur pour les communes disposant d'un faible potentiel fiscal, afin de réduire les inégalités de développement entre les différentes régions du pays.

L'amendement proposé par le Député a reçu le soutien de plusieurs de ses collègues et sera examiné lors de la prochaine session budgétaire.""",
        "categorie": "assemblee",
        "date_publication": date(2026, 3, 5),
        "en_vedette": False,
        "publie": True,
    },
    {
        "titre": "Lancement du Programme d'Appui aux Jeunes Entrepreneurs de Danané",
        "extrait": "Le Député a officiellement lancé le Programme d'Appui aux Jeunes Entrepreneurs (PAJE) dans la ville de Danané, destiné à soutenir les porteurs de projets locaux.",
        "contenu": """Le vendredi 28 février 2026, le Dr. Soumahoro Souleymane a officiellement lancé le Programme d'Appui aux Jeunes Entrepreneurs (PAJE) à Danané.

Ce programme, financé grâce aux fonds du développement local, vise à accompagner 50 jeunes entrepreneurs de la circonscription dans la création et le développement de leurs projets. Il comprend des formations en gestion d'entreprise, un accompagnement personnalisé par des mentors expérimentés et un accès à un fonds de démarrage.

Lors de la cérémonie de lancement, 12 premiers bénéficiaires ont reçu leurs kits de démarrage et leurs conventions d'accompagnement. Les secteurs ciblés incluent l'agriculture moderne, l'artisanat, le commerce et les services numériques.

Le Député a exprimé sa conviction que la jeunesse est le moteur du développement de la région : « Investir dans nos jeunes, c'est investir dans l'avenir de toute notre circonscription. »""",
        "categorie": "circonscription",
        "date_publication": date(2026, 2, 28),
        "en_vedette": False,
        "publie": True,
    },
]

created = 0
for data in articles:
    slug = slugify(data['titre'])
    if not Actualite.objects.filter(slug=slug).exists():
        Actualite.objects.create(slug=slug, **data)
        created += 1
        print(f"  ✓ Article créé : {data['titre'][:50]}...")

print(f"\n✅ {created} article(s) créé(s) ({len(articles) - created} déjà existant(s)).")

# ─── NEWSLETTER ───────────────────────────────────
abonnes_data = [
    {"prenom": "Koné", "nom": "Ibrahim", "email": "ibrahim.kone@example.ci"},
    {"prenom": "Traoré", "nom": "Aminata", "email": "aminata.traore@example.ci"},
    {"prenom": "Ouattara", "nom": "Moussa", "email": "moussa.ouattara@example.ci"},
]
created_nl = 0
for ab in abonnes_data:
    obj, c = NewsletterAbonne.objects.get_or_create(email=ab['email'], defaults=ab)
    if c:
        created_nl += 1

print(f"✅ {created_nl} abonné(s) newsletter créé(s).")
print("\n🎉 Données de démonstration insérées avec succès !")
print("   → Lancez le serveur : python manage.py runserver")
print("   → Admin             : http://127.0.0.1:8000/admin/")
print("   → Site              : http://127.0.0.1:8000/")