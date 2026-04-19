# website/management/commands/fetch_fb_posts.py
#
# Usage :
#   python manage.py fetch_fb_posts            → 10 derniers posts
#   python manage.py fetch_fb_posts --limit 20 → 20 derniers posts
#
# Cron (toutes les 6h) :
#   0 */6 * * * /path/to/venv/bin/python /path/to/manage.py fetch_fb_posts >> /var/log/fb_posts.log 2>&1

import requests
from django.core.management.base import BaseCommand
from django.conf import settings
from django.utils.dateparse import parse_datetime
from website.models import FacebookPost


# ─── Constantes ─────────────────────────────────────────────────────────────

GRAPH_VERSION = "v19.0"
PAGE_ID        = "61579911162838"   # Page du député
GRAPH_BASE     = f"https://graph.facebook.com/{GRAPH_VERSION}"

FIELDS = ",".join([
    "id",
    "message",           # texte du post
    "story",             # texte alternatif si message vide (partages, etc.)
    "created_time",      # date ISO 8601
    "full_picture",      # image du post (meilleure qualité)
    "permalink_url",     # lien permanent public
])


# ─── Commande ────────────────────────────────────────────────────────────────

class Command(BaseCommand):
    help = "Récupère les derniers posts Facebook de la page du député via Graph API."

    def add_arguments(self, parser):
        parser.add_argument(
            "--limit",
            type=int,
            default=10,
            help="Nombre de posts à récupérer (défaut : 10)",
        )

    def handle(self, *args, **options):
        limit       = options["limit"]
        access_token = getattr(settings, "FB_PAGE_ACCESS_TOKEN", "")

        if not access_token:
            self.stderr.write(self.style.ERROR(
                "FB_PAGE_ACCESS_TOKEN manquant dans settings.py"
            ))
            return

        self.stdout.write(f"→ Récupération de {limit} posts (page {PAGE_ID})…")

        # ── Appel API ────────────────────────────────────────────────────────
        url = f"{GRAPH_BASE}/{PAGE_ID}/posts"
        params = {
            "access_token": access_token,
            "fields":       FIELDS,
            "limit":        limit,
        }

        try:
            resp = requests.get(url, params=params, timeout=15)
            resp.raise_for_status()
        except requests.RequestException as e:
            self.stderr.write(self.style.ERROR(f"Erreur API Facebook : {e}"))
            return

        data  = resp.json()
        posts = data.get("data", [])

        if not posts:
            self.stdout.write(self.style.WARNING("Aucun post retourné par l'API."))
            return

        # ── Upsert ───────────────────────────────────────────────────────────
        created_count = 0
        updated_count = 0

        for i, post in enumerate(posts):
            fb_id     = post.get("id", "")
            legende   = post.get("message") or post.get("story") or ""
            image_url = post.get("full_picture") or ""
            permalink = post.get("permalink_url") or f"https://www.facebook.com/{fb_id}"
            date_post = parse_datetime(post["created_time"]) if post.get("created_time") else None

            if not fb_id or not date_post:
                self.stdout.write(self.style.WARNING(f"  Post ignoré (données incomplètes) : {post}"))
                continue

            obj, created = FacebookPost.objects.update_or_create(
                fb_id=fb_id,
                defaults={
                    "url":       permalink,
                    "legende":   legende,
                    "image_url": image_url,
                    "date_post": date_post,
                    "actif":     True,
                    "ordre":     i,     # ordre = position dans le flux (0 = le plus récent)
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