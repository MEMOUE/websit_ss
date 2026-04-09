from django.db import models
from django.utils.text import slugify
from django.urls import reverse


# ─── ACTUALITÉS ──────────────────────────────────────

class Actualite(models.Model):
    CATEGORIE_CHOICES = [
        ('assemblee', 'Assemblée Nationale'),
        ('circonscription', 'En Circonscription'),
        ('agriculture', 'Agriculture'),
        ('economie', 'Économie'),
        ('education', 'Éducation'),
        ('sante', 'Santé'),
        ('environnement', 'Environnement'),
        ('infrastructure', 'Infrastructure'),
        ('jeunesse', 'Jeunesse'),
        ('culture', 'Culture'),
        ('social', 'Social'),
        ('securite', 'Sécurité'),
        ('presse', 'Revue de Presse'),
        ('video', 'Vidéo'),
    ]
    titre            = models.CharField(max_length=255, verbose_name="Titre")
    slug             = models.SlugField(max_length=270, unique=True, blank=True)
    extrait          = models.TextField(max_length=400, verbose_name="Extrait")
    contenu          = models.TextField(verbose_name="Contenu")
    categorie        = models.CharField(max_length=30, choices=CATEGORIE_CHOICES, default='assemblee')
    image            = models.ImageField(upload_to='actualites/', blank=True, null=True)
    date_publication = models.DateField(verbose_name="Date de publication")
    en_vedette       = models.BooleanField(default=False, verbose_name="En vedette")
    publie           = models.BooleanField(default=True, verbose_name="Publié")
    created_at       = models.DateTimeField(auto_now_add=True)
    updated_at       = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Actualité"
        verbose_name_plural = "Actualités"
        ordering = ['-date_publication', '-created_at']

    def __str__(self): return self.titre

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.titre)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('website:actualite_detail', kwargs={'slug': self.slug})

    def get_categorie_display_color(self):
        mapping = {
            'assemblee': 'var(--orange)', 'circonscription': 'var(--vert)',
            'presse': '#6B7280', 'video': '#7C3AED',
        }
        return mapping.get(self.categorie, 'var(--orange)')


# ─── NEWSLETTER ──────────────────────────────────────

class NewsletterAbonne(models.Model):
    prenom           = models.CharField(max_length=100, verbose_name="Prénom")
    nom              = models.CharField(max_length=100, verbose_name="Nom")
    email            = models.EmailField(unique=True, verbose_name="E-mail")
    actif            = models.BooleanField(default=True, verbose_name="Actif")
    date_inscription = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Abonné Newsletter"
        verbose_name_plural = "Abonnés Newsletter"
        ordering = ['-date_inscription']

    def __str__(self): return f"{self.prenom} {self.nom} <{self.email}>"


# ─── CONTACT ─────────────────────────────────────────

class MessageContact(models.Model):
    SUJET_CHOICES = [
        ('demande', "Demande d'information"),
        ('suggestion', 'Suggestion / Proposition'),
        ('permanence', 'Demande de permanence'),
        ('partenariat', 'Partenariat'),
        ('autre', 'Autre'),
    ]
    nom        = models.CharField(max_length=150, verbose_name="Nom complet")
    email      = models.EmailField(verbose_name="E-mail")
    telephone  = models.CharField(max_length=20, blank=True, verbose_name="Téléphone")
    sujet      = models.CharField(max_length=30, choices=SUJET_CHOICES, default='demande')
    message    = models.TextField(verbose_name="Message")
    lu         = models.BooleanField(default=False, verbose_name="Lu")
    date_envoi = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Message de Contact"
        verbose_name_plural = "Messages de Contact"
        ordering = ['-date_envoi']

    def __str__(self):
        return f"[{self.get_sujet_display()}] {self.nom} — {self.date_envoi.strftime('%d/%m/%Y')}"


# ─── PARLEMENT ───────────────────────────────────────

class Commission(models.Model):
    TYPE_CHOICES = [('principale', 'Principale'), ('membre', 'Membre')]
    icone       = models.CharField(max_length=10, default='🏛️', verbose_name="Emoji")
    nom         = models.CharField(max_length=255, verbose_name="Nom")
    type        = models.CharField(max_length=20, choices=TYPE_CHOICES, default='membre')
    description = models.TextField(verbose_name="Description")
    ordre       = models.PositiveIntegerField(default=0, verbose_name="Ordre")

    class Meta:
        verbose_name = "Commission"
        verbose_name_plural = "Commissions"
        ordering = ['ordre']

    def __str__(self): return self.nom


class Intervention(models.Model):
    date        = models.DateField(verbose_name="Date")
    contexte    = models.CharField(max_length=100, verbose_name="Contexte (ex: Séance plénière)")
    titre       = models.CharField(max_length=255, verbose_name="Titre")
    description = models.TextField(verbose_name="Description")
    tag         = models.CharField(max_length=60, verbose_name="Étiquette")

    class Meta:
        verbose_name = "Intervention"
        verbose_name_plural = "Interventions"
        ordering = ['-date']

    def __str__(self): return f"{self.date} — {self.titre}"


class TexteLoi(models.Model):
    TYPE_CHOICES = [
        ('amendement',      'Amendement'),
        ('question_ecrite', 'Question écrite'),
        ('question_orale',  'Question orale'),
        ('resolution',      'Proposition de résolution'),
    ]
    icone = models.CharField(max_length=10, default='📜', verbose_name="Emoji")
    type  = models.CharField(max_length=30, choices=TYPE_CHOICES, verbose_name="Type")
    titre = models.CharField(max_length=255, verbose_name="Titre")
    meta  = models.CharField(max_length=255, verbose_name="Date & statut")
    ordre = models.PositiveIntegerField(default=0, verbose_name="Ordre")

    class Meta:
        verbose_name = "Texte / Proposition"
        verbose_name_plural = "Textes & Propositions"
        ordering = ['ordre']

    def __str__(self): return self.titre


# ─── CIRCONSCRIPTION ─────────────────────────────────

class Commune(models.Model):
    icone         = models.CharField(max_length=10, default='🏙️', verbose_name="Emoji")
    nom           = models.CharField(max_length=100, verbose_name="Nom")
    type_commune  = models.CharField(max_length=100, default='Sous-Préfecture', verbose_name="Type")
    population    = models.CharField(max_length=60, blank=True, verbose_name="Population")
    description   = models.TextField(blank=True, verbose_name="Description courte")
    projets       = models.TextField(blank=True, verbose_name="Projets (1 par ligne)")
    ordre         = models.PositiveIntegerField(default=0, verbose_name="Ordre")

    class Meta:
        verbose_name = "Commune"
        verbose_name_plural = "Communes"
        ordering = ['ordre']

    def __str__(self): return self.nom

    def get_projets_list(self):
        return [p.strip() for p in self.projets.splitlines() if p.strip()]


class Permanence(models.Model):
    date        = models.DateField(verbose_name="Date")
    titre       = models.CharField(max_length=200, verbose_name="Titre")
    lieu        = models.CharField(max_length=200, verbose_name="Lieu")
    heure_debut = models.TimeField(verbose_name="Heure de début", null=True, blank=True)
    heure_fin   = models.TimeField(verbose_name="Heure de fin",   null=True, blank=True)
    passee      = models.BooleanField(default=False, verbose_name="Passée")

    class Meta:
        verbose_name = "Permanence"
        verbose_name_plural = "Permanences"
        ordering = ['-date']

    def __str__(self): return f"{self.date} — {self.titre}"

    def get_heure(self):
        if self.heure_debut and self.heure_fin:
            return f"{self.heure_debut.strftime('%Hh%M')} – {self.heure_fin.strftime('%Hh%M')}"
        elif self.heure_debut:
            return self.heure_debut.strftime('%Hh%M')
        return ""


# ─── AGENDA ──────────────────────────────────────────

class EvenementAgenda(models.Model):
    TYPE_CHOICES = [
        ('assemblee',       'Assemblée Nationale'),
        ('circonscription', 'En Circonscription'),
        ('public',          'Événement Public'),
        ('autre',           'Autre'),
    ]
    STATUT_CHOICES = [
        ('avenir',  'À venir'),
        ('realise', 'Tenu'),
        ('annule',  'Annulé'),
    ]
    date        = models.DateField(verbose_name="Date")
    type        = models.CharField(max_length=20, choices=TYPE_CHOICES, default='assemblee')
    titre       = models.CharField(max_length=255, verbose_name="Titre")
    heure_debut = models.TimeField(verbose_name="Heure de début", null=True, blank=True)
    heure_fin   = models.TimeField(verbose_name="Heure de fin",   null=True, blank=True)
    lieu        = models.CharField(max_length=200, blank=True, verbose_name="Lieu")
    statut      = models.CharField(max_length=20, choices=STATUT_CHOICES, default='avenir')
    en_avant    = models.BooleanField(default=False, verbose_name="Mettre en avant")

    class Meta:
        verbose_name = "Événement"
        verbose_name_plural = "Événements Agenda"
        ordering = ['-date']

    def __str__(self): return f"{self.date} — {self.titre}"

    def get_heure(self):
        if self.heure_debut and self.heure_fin:
            return f"{self.heure_debut.strftime('%Hh%M')} – {self.heure_fin.strftime('%Hh%M')}"
        elif self.heure_debut:
            return self.heure_debut.strftime('%Hh%M')
        return ""


# ─── FACEBOOK POSTS ──────────────────────────────────

class FacebookPost(models.Model):
    """
    Chaque entrée représente un post Facebook à afficher en card sur la page d'accueil.
    Ajouter l'URL complète du post depuis la page Facebook officielle.
    Exemple d'URL : https://www.facebook.com/profile.php?id=61579911162838&posts/123456789
    """
    url        = models.URLField(
        max_length=500,
        verbose_name="URL du post Facebook",
        help_text="Copiez l'URL complète du post (clic droit sur la date du post → Copier l'adresse du lien)"
    )
    legende    = models.CharField(
        max_length=200, blank=True,
        verbose_name="Légende (optionnelle)",
        help_text="Courte description affichée si l'embed ne charge pas"
    )
    actif      = models.BooleanField(default=True, verbose_name="Afficher sur le site")
    ordre      = models.PositiveIntegerField(default=0, verbose_name="Ordre d'affichage")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Publication Facebook"
        verbose_name_plural = "Publications Facebook"
        ordering = ['ordre', '-created_at']

    def __str__(self):
        return self.legende or self.url[:60]