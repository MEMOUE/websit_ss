import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'website_ss.settings')
django.setup()

from website.models import ProjetFondation

PROJETS = [
    {
        "icone": "📚",
        "titre": "Bourses Scolaires Tonpki 2026",
        "description": "Attribution de 50 bourses scolaires aux élèves méritants issus de familles défavorisées des cinq communes. Le programme couvre les frais de scolarité, les fournitures et l'accompagnement pédagogique tout au long de l'année.",
        "domaine": "education",
        "statut": "en_cours",
        "beneficiaires": "50 élèves du primaire et secondaire",
        "lieu": "Daleu · Danané · Gbon-Houyé · Kouan-Houlé · Seileu",
        "ordre": 1,
    },
    {
        "icone": "🏫",
        "titre": "Réhabilitation de l'École Primaire de Seileu",
        "description": "Rénovation complète de trois salles de classe, construction de latrines et installation de points d'eau potable dans l'enceinte scolaire. Le projet améliore les conditions d'apprentissage pour plus de 200 élèves.",
        "domaine": "education",
        "statut": "realise",
        "beneficiaires": "200+ élèves, enseignants",
        "lieu": "Seileu",
        "ordre": 2,
    },
    {
        "icone": "🚀",
        "titre": "Centre de Formation Professionnelle — Danané",
        "description": "Création d'un centre de formation aux métiers du numérique, de la couture et de l'électricité. 80 jeunes de 18 à 30 ans seront formés et accompagnés vers l'emploi ou la création de micro-entreprises locales.",
        "domaine": "jeunesse",
        "statut": "en_cours",
        "beneficiaires": "80 jeunes 18–30 ans",
        "lieu": "Danané",
        "ordre": 3,
    },
    {
        "icone": "💼",
        "titre": "Fonds d'Amorçage Jeunes Entrepreneurs",
        "description": "Micro-crédits sans intérêt de 50 000 à 200 000 FCFA accordés à de jeunes porteurs de projets agricoles, artisanaux ou commerciaux. Chaque bénéficiaire est suivi par un mentor pendant six mois.",
        "domaine": "jeunesse",
        "statut": "planifie",
        "beneficiaires": "30 jeunes entrepreneurs",
        "lieu": "Circonscription de Danané",
        "ordre": 4,
    },
    {
        "icone": "🌱",
        "titre": "Agriculture Durable & Sécurité Alimentaire",
        "description": "Distribution de semences améliorées, formation aux techniques de compostage et d'irrigation à faible coût. Le projet vise à augmenter les rendements agricoles de 30 % pour les petits exploitants des zones rurales.",
        "domaine": "communaute",
        "statut": "en_cours",
        "beneficiaires": "120 exploitants agricoles",
        "lieu": "Gbon-Houyé · Kouan-Houlé",
        "ordre": 5,
    },
    {
        "icone": "🏥",
        "titre": "Caravane de Santé Communautaire",
        "description": "Consultations médicales gratuites, dépistage du paludisme et de l'hypertension, distribution de moustiquaires imprégnées. La caravane se déplace dans les villages reculés deux fois par trimestre.",
        "domaine": "sante",
        "statut": "realise",
        "beneficiaires": "500+ habitants des zones rurales",
        "lieu": "Daleu · Gbon-Houyé · Seileu",
        "ordre": 6,
    },
    {
        "icone": "💧",
        "titre": "Adduction d'Eau Potable — Villages de Kouan-Houlé",
        "description": "Installation de deux forages équipés de pompes solaires pour approvisionner en eau potable trois villages de la sous-préfecture, réduisant ainsi les maladies hydriques saisonnières.",
        "domaine": "communaute",
        "statut": "planifie",
        "beneficiaires": "~800 habitants",
        "lieu": "Kouan-Houlé",
        "ordre": 7,
    },
    {
        "icone": "📖",
        "titre": "Bibliothèques Numériques Mobiles",
        "description": "Déploiement de tablettes éducatives préchargées avec des contenus pédagogiques offline dans cinq écoles primaires. Chaque école reçoit 20 tablettes et une formation pour les enseignants.",
        "domaine": "education",
        "statut": "planifie",
        "beneficiaires": "5 écoles, ~600 élèves",
        "lieu": "Daleu · Danané · Gbon-Houyé · Kouan-Houlé · Seileu",
        "ordre": 8,
    },
    {
        "icone": "👩‍🍳",
        "titre": "Autonomisation des Femmes — Groupements Coopératifs",
        "description": "Structuration et accompagnement de groupements féminins en coopératives formelles : formation à la gestion, accès au crédit et mise en marché de produits transformés (attiéké, huile de palme, savon artisanal).",
        "domaine": "communaute",
        "statut": "en_cours",
        "beneficiaires": "60 femmes en 4 groupements",
        "lieu": "Danané · Daleu",
        "ordre": 9,
    },
]

created = updated = 0
for data in PROJETS:
    obj, is_new = ProjetFondation.objects.update_or_create(
        titre=data['titre'],
        defaults=data,
    )
    if is_new:
        created += 1
        print(f"  ✚ Créé  : {obj.titre}")
    else:
        updated += 1
        print(f"  ↺ Màj   : {obj.titre}")

print(f"\n✔ Terminé : {created} créé(s), {updated} mis à jour.")
print(f"  Total en base : {ProjetFondation.objects.count()} projet(s).")