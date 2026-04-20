# website/management/commands/sync_facebook.py
#
# Usage :
#   python manage.py sync_facebook            → 10 derniers posts
#   python manage.py sync_facebook --limit 20 → 20 derniers posts
#
# Cron (toutes les 6h) :
#   0 */6 * * * /chemin/venv/bin/python /chemin/manage.py sync_facebook >> /var/log/fb.log 2>&1

import requests
from django.core.management.base import BaseCommand
from django.conf import settings
from django.utils.dateparse import parse_datetime
from website.models import FacebookPost

GRAPH_VERSION = "v19.0"
PAGE_ID       = "61579911162838"
GRAPH_BASE    = f"https://graph.facebook.com/{GRAPH_VERSION}"
FIELDS        = "id,message,story,created_time,full_picture,permalink_url"


class Command(BaseCommand):
    help = "Synchronise les derniers posts Facebook de la page du député."

    def add_arguments(self, parser):
        parser.add_argument(
            "--limit", type=int, default=10,
            help="Nombre de posts à récupérer (défaut : 10)",
        )

    def handle(self, *args, **options):
        limit        = options["limit"]
        access_token = getattr(settings, "FB_PAGE_ACCESS_TOKEN", "")

        if not access_token:
            self.stderr.write(self.style.ERROR(
                "FB_PAGE_ACCESS_TOKEN manquant dans settings.py"
            ))
            return

        self.stdout.write(f"→ Récupération de {limit} posts (page {PAGE_ID})…")

        try:
            resp = requests.get(
                f"{GRAPH_BASE}/{PAGE_ID}/posts",
                params={"access_token": access_token, "fields": FIELDS, "limit": limit},
                timeout=15,
            )
            resp.raise_for_status()
        except requests.RequestException as e:
            self.stderr.write(self.style.ERROR(f"Erreur API Facebook : {e}"))
            return

        posts = resp.json().get("data", [])

        if not posts:
            self.stdout.write(self.style.WARNING("Aucun post retourné par l'API."))
            return

        created_count = updated_count = 0

        for i, post in enumerate(posts):
            fb_id     = post.get("id", "")
            legende   = post.get("message") or post.get("story") or ""
            image_url = post.get("full_picture") or ""
            permalink = post.get("permalink_url") or f"https://www.facebook.com/{fb_id}"
            date_post = parse_datetime(post["created_time"]) if post.get("created_time") else None

            if not fb_id or not date_post:
                self.stdout.write(self.style.WARNING(f"  Post ignoré : {post}"))
                continue

            _, created = FacebookPost.objects.update_or_create(
                fb_id=fb_id,
                defaults={
                    "url":       permalink,
                    "legende":   legende,
                    "image_url": image_url,
                    "date_post": date_post,
                    "actif":     True,
                    "ordre":     i,
                },
            )

            if created:
                created_count += 1
                self.stdout.write(f"  ✚ Créé  : {fb_id} — {legende[:60]}")
            else:
                updated_count += 1
                self.stdout.write(f"  ↺ Màj   : {fb_id} — {legende[:60]}")

        self.stdout.write(self.style.SUCCESS(
            f"\n✔ Terminé : {created_count} créé(s), {updated_count} mis à jour."
        ))