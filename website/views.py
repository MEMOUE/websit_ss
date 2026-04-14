from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator

from .models import (Actualite, NewsletterAbonne, MessageContact,
                     Commission, Intervention, TexteLoi,
                     Commune, Permanence, EvenementAgenda, FacebookPost)
from .forms import NewsletterForm, ContactForm
from itertools import groupby


# ─────────────────────────────────────────
#  PAGE D'ACCUEIL
# ─────────────────────────────────────────
def index(request):
    """Page d'accueil : hero + dernières actualités + posts Facebook + newsletter."""
    en_vedette = Actualite.objects.filter(publie=True, en_vedette=True).first()

    actualites_recentes = Actualite.objects.filter(publie=True)
    if en_vedette:
        actualites_recentes = actualites_recentes.exclude(pk=en_vedette.pk)
    actualites_recentes = actualites_recentes[:1]

    # 10 dernières publications Facebook actives
    fb_posts = FacebookPost.objects.filter(actif=True)[:4]

    nl_form = NewsletterForm()

    context = {
        'en_vedette':          en_vedette,
        'actualites_recentes': actualites_recentes,
        'nl_form':             nl_form,
        'nb_abonnes':          NewsletterAbonne.objects.filter(actif=True).count(),
        'fb_posts':            fb_posts,
    }
    return render(request, 'index.html', context)


# ─────────────────────────────────────────
#  LISTE DES ACTUALITÉS
# ─────────────────────────────────────────
def actualites(request):
    categorie = request.GET.get('categorie', '')
    qs = Actualite.objects.filter(publie=True)
    if categorie:
        qs = qs.filter(categorie=categorie)
    paginator = Paginator(qs, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj':         page_obj,
        'categories':       Actualite.CATEGORIE_CHOICES,
        'categorie_active': categorie,
    }
    return render(request, 'actualites.html', context)


# ─────────────────────────────────────────
#  DÉTAIL D'UN ARTICLE
# ─────────────────────────────────────────
def actualite_detail(request, slug):
    article = get_object_or_404(Actualite, slug=slug, publie=True)
    articles_lies = Actualite.objects.filter(
        publie=True, categorie=article.categorie
    ).exclude(pk=article.pk)[:3]
    return render(request, 'actualite_detail.html', {
        'article':       article,
        'articles_lies': articles_lies,
    })


# ─────────────────────────────────────────
#  INSCRIPTION NEWSLETTER
# ─────────────────────────────────────────
@require_POST
def newsletter_inscription(request):
    form = NewsletterForm(request.POST)
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    if form.is_valid():
        abonne = form.save()
        try:
            send_mail(
                subject="Confirmation d'inscription à la newsletter",
                message=(
                    f"Bonjour {abonne.prenom},\n\n"
                    "Vous êtes bien inscrit(e) à la newsletter du Député Dr. Soumahoro Souleymane.\n\n"
                    "Vous recevrez bientôt nos prochaines communications.\n\n"
                    "— Équipe du Député"
                ),
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[abonne.email],
                fail_silently=True,
            )
        except Exception:
            pass
        if is_ajax:
            return JsonResponse({'success': True, 'message': 'Inscription confirmée !'})
        messages.success(request, f"Merci {abonne.prenom} ! Votre inscription est confirmée.")
        return redirect('website:index')
    if is_ajax:
        return JsonResponse({'success': False, 'errors': form.errors.as_json()}, status=400)
    messages.error(request, "Formulaire invalide. Veuillez vérifier vos informations.")
    return redirect('website:index')


# ─────────────────────────────────────────
#  FORMULAIRE DE CONTACT
# ─────────────────────────────────────────
def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            msg = form.save()
            try:
                send_mail(
                    subject=f"[Contact Site] {msg.get_sujet_display()} — {msg.nom}",
                    message=(
                        f"Nouveau message de contact reçu.\n\n"
                        f"Nom     : {msg.nom}\n"
                        f"Email   : {msg.email}\n"
                        f"Tél.    : {msg.telephone or 'Non renseigné'}\n"
                        f"Sujet   : {msg.get_sujet_display()}\n\n"
                        f"Message :\n{msg.message}"
                    ),
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[settings.CONTACT_EMAIL],
                    fail_silently=True,
                )
            except Exception:
                pass
            messages.success(
                request,
                "Votre message a bien été envoyé. Nous vous répondrons dans les meilleurs délais."
            )
            return redirect('website:contact')
    else:
        form = ContactForm()
    return render(request, 'contact.html', {'form': form})


# ─────────────────────────────────────────
#  PAGES STATIQUES
# ─────────────────────────────────────────
def parlement(request):
    context = {
        'commissions':   Commission.objects.all(),
        'interventions': Intervention.objects.all()[:6],
        'textes':        TexteLoi.objects.all(),
    }
    return render(request, 'parlement.html', context)


def circonscription(request):
    context = {
        'communes':            Commune.objects.all(),
        'permanences_avenir':  Permanence.objects.filter(passee=False).order_by('date'),
        'permanences_passees': Permanence.objects.filter(passee=True)[:3],
    }
    return render(request, 'circonscription.html', context)


def agenda(request):
    MOIS = ['Janvier', 'Février', 'Mars', 'Avril', 'Mai', 'Juin',
            'Juillet', 'Août', 'Septembre', 'Octobre', 'Novembre', 'Décembre']
    evenements = EvenementAgenda.objects.all()
    groupes = []
    for key, group in groupby(evenements, key=lambda e: (e.date.year, e.date.month)):
        groupes.append({
            'label':      f"{MOIS[key[1]-1]} {key[0]}",
            'evenements': list(group)
        })
    return render(request, 'agenda.html', {'groupes': groupes})