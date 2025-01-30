from django import forms
from .models import ContactBase


class ContactForm(forms.ModelForm):
    """
    Formulaire basé sur le modèle ContactBase.

    Ce formulaire permet de collecter les informations suivantes :
    - name : Nom de la personne qui contacte.
    - mail : Adresse e-mail de la personne.
    - subject : Sujet du message.
    - message : Contenu du message.

    Attributs :
    -----------
    model : ContactBase
        Modèle associé au formulaire.
    fields : list
        Liste des champs inclus dans le formulaire.
    """
    class Meta:
        model = ContactBase  # Modèle associé au formulaire.
        fields = ['name', 'mail', 'subject', 'message']  # Champs inclus dans le formulaire.