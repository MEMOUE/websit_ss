from django.contrib import admin
from django.utils.html import format_html
from .models import (Actualite, NewsletterAbonne, MessageContact,
                     Commission, Intervention, TexteLoi,
                     Commune, Permanence, EvenementAgenda, FacebookPost)


@admin.register(Actualite)
class ActualiteAdmin(admin.ModelAdmin):
    list_display        = ('titre', 'categorie', 'date_publication', 'en_vedette', 'publie', 'apercu_image')
    list_filter         = ('categorie', 'publie', 'en_vedette')
    search_fields       = ('titre', 'extrait')
    prepopulated_fields = {'slug': ('titre',)}
    list_editable       = ('publie', 'en_vedette')
    date_hierarchy      = 'date_publication'
    fieldsets = (
        ('Informations', {'fields': ('titre', 'slug', 'categorie', 'date_publication', 'image')}),
        ('Contenu',      {'fields': ('extrait', 'contenu')}),
        ('Publication',  {'fields': ('publie', 'en_vedette'), 'classes': ('collapse',)}),
    )
    def apercu_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="width:60px;height:40px;object-fit:cover;border-radius:4px;"/>', obj.image.url)
        return "—"
    apercu_image.short_description = "Image"


@admin.register(NewsletterAbonne)
class NewsletterAbonneAdmin(admin.ModelAdmin):
    list_display    = ('prenom', 'nom', 'email', 'actif', 'date_inscription')
    list_filter     = ('actif',)
    search_fields   = ('email', 'nom')
    list_editable   = ('actif',)
    readonly_fields = ('date_inscription',)


@admin.register(MessageContact)
class MessageContactAdmin(admin.ModelAdmin):
    list_display    = ('nom', 'email', 'sujet', 'date_envoi', 'lu')
    list_filter     = ('sujet', 'lu')
    list_editable   = ('lu',)
    readonly_fields = ('nom', 'email', 'telephone', 'sujet', 'message', 'date_envoi')
    def has_add_permission(self, request): return False


# ─── PARLEMENT ───
@admin.register(Commission)
class CommissionAdmin(admin.ModelAdmin):
    list_display  = ('icone', 'nom', 'type', 'ordre')
    list_editable = ('type', 'ordre')

@admin.register(Intervention)
class InterventionAdmin(admin.ModelAdmin):
    list_display  = ('date', 'titre', 'contexte', 'tag')
    date_hierarchy = 'date'

@admin.register(TexteLoi)
class TexteLoiAdmin(admin.ModelAdmin):
    list_display  = ('icone', 'type', 'titre', 'meta', 'ordre')
    list_editable = ('ordre',)
    list_filter   = ('type',)


# ─── CIRCONSCRIPTION ───
@admin.register(Commune)
class CommuneAdmin(admin.ModelAdmin):
    list_display  = ('icone', 'nom', 'type_commune', 'population', 'ordre')
    list_editable = ('ordre',)

@admin.register(Permanence)
class PermanenceAdmin(admin.ModelAdmin):
    list_display  = ('date', 'titre', 'lieu', 'heure_debut', 'heure_fin', 'passee')
    list_editable = ('passee',)
    list_filter   = ('passee',)
    date_hierarchy = 'date'
    fields        = ('date', 'titre', 'lieu', ('heure_debut', 'heure_fin'), 'passee')


@admin.register(EvenementAgenda)
class EvenementAgendaAdmin(admin.ModelAdmin):
    list_display  = ('date', 'titre', 'type', 'lieu', 'heure_debut', 'heure_fin', 'statut', 'en_avant')
    list_editable = ('type', 'statut', 'en_avant')
    list_filter   = ('type', 'statut')
    date_hierarchy = 'date'
    fields        = ('date', 'type', 'titre', ('heure_debut', 'heure_fin'), 'lieu', 'statut', 'en_avant')


# ─── FACEBOOK POSTS ───
@admin.register(FacebookPost)
class FacebookPostAdmin(admin.ModelAdmin):
    list_display  = ('legende_ou_url', 'actif', 'ordre', 'created_at', 'apercu_lien')
    list_editable = ('actif', 'ordre')
    list_filter   = ('actif',)
    fields        = ('url', 'legende', 'actif', 'ordre')
    ordering      = ('ordre', '-created_at')

    def legende_ou_url(self, obj):
        return obj.legende or obj.url[:60] + ('…' if len(obj.url) > 60 else '')
    legende_ou_url.short_description = 'Publication'

    def apercu_lien(self, obj):
        return format_html(
            '<a href="{}" target="_blank" rel="noopener" '
            'style="color:#1877F2;font-size:12px;">Voir le post →</a>',
            obj.url
        )
    apercu_lien.short_description = 'Lien'


# Interface admin
admin.site.site_header  = "Dr. Soumahoro Souleymane — Administration"
admin.site.site_title   = "Admin Soumahoro"
admin.site.index_title  = "Tableau de bord"