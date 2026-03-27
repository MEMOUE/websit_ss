from django.db import models
from django.utils.text import slugify
from django.urls import reverse
import os


class Actualite(models.Model):
    """Article d'actualité du député."""

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

    titre       = models.CharField(max_length=255, verbose_name="Titre")
    slug        = models.SlugField(max_length=270, unique=True, blank=True, verbose_name="Slug URL")
    extrait     = models.TextField(max_length=400, verbose_name="Extrait / chapô")
    contenu     = models.TextField(verbose_name="Contenu complet")
    categorie   = models.CharField(max_length=30, choices=CATEGORIE_CHOICES,
                                   default='assemblee', verbose_name="Catégorie")
    image       = models.ImageField(upload_to='actualites/', blank=True, null=True,
                                    verbose_name="Image principale")
    date_publication = models.DateField(verbose_name="Date de publication")
    en_vedette  = models.BooleanField(default=False, verbose_name="Article en vedette (featured)")
    publie      = models.BooleanField(default=True, verbose_name="Publié")
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Actualité"
        verbose_name_plural = "Actualités"
        ordering = ['-date_publication', '-created_at']

    def __str__(self):
        return self.titre

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.titre)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('website:actualite_detail', kwargs={'slug': self.slug})

    def get_categorie_display_color(self):
        """Retourne la variable CSS couleur selon la catégorie."""
        mapping = {
            'assemblee':       'var(--orange)',
            'circonscription': 'var(--vert)',
            'presse':          '#6B7280',
            'video':           '#7C3AED',
        }
        return mapping.get(self.categorie, 'var(--orange)')


class NewsletterAbonne(models.Model):
    """Abonné à la newsletter du député."""

    prenom      = models.CharField(max_length=100, verbose_name="Prénom")
    nom         = models.CharField(max_length=100, verbose_name="Nom")
    email       = models.EmailField(unique=True, verbose_name="Adresse e-mail")
    actif       = models.BooleanField(default=True, verbose_name="Abonnement actif")
    date_inscription = models.DateTimeField(auto_now_add=True, verbose_name="Date d'inscription")

    class Meta:
        verbose_name = "Abonné Newsletter"
        verbose_name_plural = "Abonnés Newsletter"
        ordering = ['-date_inscription']

    def __str__(self):
        return f"{self.prenom} {self.nom} <{self.email}>"


class MessageContact(models.Model):
    """Message envoyé via le formulaire de contact."""

    SUJET_CHOICES = [
        ('demande',      'Demande d\'information'),
        ('suggestion',   'Suggestion / Proposition'),
        ('permanence',   'Demande de permanence'),
        ('partenariat',  'Partenariat'),
        ('autre',        'Autre'),
    ]

    nom         = models.CharField(max_length=150, verbose_name="Nom complet")
    email       = models.EmailField(verbose_name="Adresse e-mail")
    telephone   = models.CharField(max_length=20, blank=True, verbose_name="Téléphone")
    sujet       = models.CharField(max_length=30, choices=SUJET_CHOICES,
                                   default='demande', verbose_name="Sujet")
    message     = models.TextField(verbose_name="Message")
    lu          = models.BooleanField(default=False, verbose_name="Message lu")
    date_envoi  = models.DateTimeField(auto_now_add=True, verbose_name="Date d'envoi")

    class Meta:
        verbose_name = "Message de Contact"
        verbose_name_plural = "Messages de Contact"
        ordering = ['-date_envoi']

    def __str__(self):
        return f"[{self.get_sujet_display()}] {self.nom} — {self.date_envoi.strftime('%d/%m/%Y')}"