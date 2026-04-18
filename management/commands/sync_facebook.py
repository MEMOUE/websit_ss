import requests
from django.core.management.base import BaseCommand
from website.models import FacebookPost
from django.utils.dateparse import parse_datetime


class Command(BaseCommand):
    help = "Récupère automatiquement les derniers posts de la page Facebook"

    def handle(self, *args, **options):
        # Configuration (À mettre idéalement dans vos settings)
        PAGE_ID = "61579911162838"
        ACCESS_TOKEN = "VOTRE_PAGE_ACCESS_TOKEN"  # Obtenu via Meta for Developers

        url = f"https://graph.facebook.com/v18.0/{PAGE_ID}/posts"
        params = {
            'fields': 'id,message,permalink_url,full_picture,created_time',
            'access_token': ACCESS_TOKEN,
            'limit': 10  # Récupère les 10 derniers
        }

        try:
            response = requests.get(url, params=params)
            data = response.json()

            for post in data.get('data', []):
                # update_or_create évite les doublons si le script tourne plusieurs fois
                FacebookPost.objects.update_or_create(
                    fb_id=post['id'],
                    defaults={
                        'url': post.get('permalink_url'),
                        'legende': post.get('message', ""),
                        'image_url': post.get('full_picture'),
                        'date_post': parse_datetime(post['created_time']),
                        'actif': True
                    }
                )
            self.stdout.write(self.style.SUCCESS('Synchronisation Facebook réussie !'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Erreur : {e}'))