from django.contrib import admin
from django.utils.html import format_html
from .models import Actualite, NewsletterAbonne, MessageContact


@admin.register(Actualite)
class ActualiteAdmin(admin.ModelAdmin):
    list_display    = ('titre', 'categorie', 'date_publication', 'en_vedette', 'publie', 'apercu_image')
    list_filter     = ('categorie', 'publie', 'en_vedette', 'date_publication')
    search_fields   = ('titre', 'extrait', 'contenu')
    prepopulated_fields = {'slug': ('titre',)}
    list_editable   = ('publie', 'en_vedette')
    date_hierarchy  = 'date_publication'
    ordering        = ('-date_publication',)
    fieldsets = (
        ('Informations principales', {
            'fields': ('titre', 'slug', 'categorie', 'date_publication', 'image')
        }),
        ('Contenu', {
            'fields': ('extrait', 'contenu')
        }),
        ('Publication', {
            'fields': ('publie', 'en_vedette'),
            'classes': ('collapse',),
        }),
    )

    def apercu_image(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="width:60px;height:40px;object-fit:cover;border-radius:4px;" />',
                obj.image.url
            )
        return "—"
    apercu_image.short_description = "Aperçu"


@admin.register(NewsletterAbonne)
class NewsletterAbonneAdmin(admin.ModelAdmin):
    list_display  = ('prenom', 'nom', 'email', 'actif', 'date_inscription')
    list_filter   = ('actif',)
    search_fields = ('prenom', 'nom', 'email')
    list_editable = ('actif',)
    readonly_fields = ('date_inscription',)
    actions = ['desactiver_abonnes', 'exporter_emails']

    def desactiver_abonnes(self, request, queryset):
        updated = queryset.update(actif=False)
        self.message_user(request, f"{updated} abonné(s) désactivé(s).")
    desactiver_abonnes.short_description = "Désactiver les abonnés sélectionnés"

    def exporter_emails(self, request, queryset):
        emails = ", ".join(queryset.filter(actif=True).values_list('email', flat=True))
        self.message_user(request, f"Emails actifs : {emails}")
    exporter_emails.short_description = "Afficher les e-mails actifs sélectionnés"


@admin.register(MessageContact)
class MessageContactAdmin(admin.ModelAdmin):
    list_display  = ('nom', 'email', 'sujet', 'date_envoi', 'lu')
    list_filter   = ('sujet', 'lu', 'date_envoi')
    search_fields = ('nom', 'email', 'message')
    list_editable = ('lu',)
    readonly_fields = ('nom', 'email', 'telephone', 'sujet', 'message', 'date_envoi')
    ordering = ('-date_envoi',)

    def has_add_permission(self, request):
        return False  # Les messages viennent uniquement du formulaire


# Personnalisation de l'interface Admin
admin.site.site_header  = "Dr. Soumahoro Souleymane — Administration"
admin.site.site_title   = "Admin Soumahoro"
admin.site.index_title  = "Tableau de bord"