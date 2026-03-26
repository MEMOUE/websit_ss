from django import forms
from .models import NewsletterAbonne, MessageContact


class NewsletterForm(forms.ModelForm):
    class Meta:
        model = NewsletterAbonne
        fields = ['prenom', 'nom', 'email']
        widgets = {
            'prenom': forms.TextInput(attrs={
                'class': 'nl-input',
                'placeholder': 'Votre prénom',
            }),
            'nom': forms.TextInput(attrs={
                'class': 'nl-input',
                'placeholder': 'Votre nom',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'nl-input',
                'placeholder': 'Votre adresse e-mail',
            }),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if NewsletterAbonne.objects.filter(email=email, actif=True).exists():
            raise forms.ValidationError("Cette adresse e-mail est déjà inscrite à la newsletter.")
        return email


class ContactForm(forms.ModelForm):
    class Meta:
        model = MessageContact
        fields = ['nom', 'email', 'telephone', 'sujet', 'message']
        widgets = {
            'nom': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Votre nom complet',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-input',
                'placeholder': 'votre@email.com',
            }),
            'telephone': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': '+225 XX XX XX XX XX',
            }),
            'sujet': forms.Select(attrs={
                'class': 'form-input',
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-input',
                'placeholder': 'Votre message...',
                'rows': 6,
            }),
        }
        labels = {
            'nom':       'Nom complet *',
            'email':     'Adresse e-mail *',
            'telephone': 'Téléphone (optionnel)',
            'sujet':     'Objet *',
            'message':   'Message *',
        }