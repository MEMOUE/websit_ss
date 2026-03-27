from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator

from .models import Actualite, NewsletterAbonne, MessageContact
from .forms import NewsletterForm, ContactForm


# ─────────────────────────────────────────
#  PAGE D'ACCUEIL
# ─────────────────────────────────────────
def index(request):
    """Page d'accueil : hero + dernières actualités + newsletter."""
    # Article en vedette
    en_vedette = Actualite.objects.filter(publie=True, en_vedette=True).first()

    # Les 4 derniers articles publiés (hors vedette)
    actualites_recentes = Actualite.objects.filter(publie=True)
    if en_vedette:
        actualites_recentes = actualites_recentes.exclude(pk=en_vedette.pk)
    actualites_recentes = actualites_recentes[:1]

    # Formulaire newsletter
    nl_form = NewsletterForm()

    context = {
        'en_vedette':         en_vedette,
        'actualites_recentes': actualites_recentes,
        'nl_form':            nl_form,
        'nb_abonnes':         NewsletterAbonne.objects.filter(actif=True).count(),
    }
    return render(request, 'index.html', context)


# ─────────────────────────────────────────
#  LISTE DES ACTUALITÉS
# ─────────────────────────────────────────
def actualites(request):
    """Liste paginée de toutes les actualités avec filtre catégorie."""
    categorie = request.GET.get('categorie', '')
    qs = Actualite.objects.filter(publie=True)

    if categorie:
        qs = qs.filter(categorie=categorie)

    paginator = Paginator(qs, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    categories = Actualite.CATEGORIE_CHOICES

    context = {
        'page_obj':   page_obj,
        'categories': categories,
        'categorie_active': categorie,
    }
    return render(request, 'actualites.html', context)


# ─────────────────────────────────────────
#  DÉTAIL D'UN ARTICLE
# ─────────────────────────────────────────
def actualite_detail(request, slug):
    """Page de détail d'un article."""
    article = get_object_or_404(Actualite, slug=slug, publie=True)

    # Articles liés (même catégorie, 3 max)
    articles_lies = Actualite.objects.filter(
        publie=True, categorie=article.categorie
    ).exclude(pk=article.pk)[:3]

    context = {
        'article':      article,
        'articles_lies': articles_lies,
    }
    return render(request, 'actualite_detail.html', context)


# ─────────────────────────────────────────
#  INSCRIPTION NEWSLETTER (AJAX + normal)
# ─────────────────────────────────────────
@require_POST
def newsletter_inscription(request):
    """Traitement du formulaire newsletter (POST — supporte AJAX)."""
    form = NewsletterForm(request.POST)
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'

    if form.is_valid():
        abonne = form.save()

        # E-mail de confirmation (console en dev)
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
        errors = form.errors.as_json()
        return JsonResponse({'success': False, 'errors': errors}, status=400)

    messages.error(request, "Formulaire invalide. Veuillez vérifier vos informations.")
    return redirect('website:index')


# ─────────────────────────────────────────
#  FORMULAIRE DE CONTACT
# ─────────────────────────────────────────
def contact(request):
    """Page de contact avec formulaire."""
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            msg = form.save()

            # Notification e-mail à l'équipe
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

def parlement(request):
    return render(request, 'parlement.html', {})

def circonscription(request):
    return render(request, 'circonscription.html', {})

def agenda(request):
    return render(request, 'agenda.html', {})