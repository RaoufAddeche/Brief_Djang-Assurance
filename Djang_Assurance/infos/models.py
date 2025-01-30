from django.db import models

# Définition des modèles ici.


class ContactBase(models.Model):
    """
    Modèle représentant un contact.

    Attributs :
    -----------
    name : CharField
        Nom de la personne qui contacte (obligatoire, max 100 caractères).
    mail : CharField
        Adresse e-mail de la personne (obligatoire, max 250 caractères).
    subject : CharField
        Sujet du message (facultatif, max 100 caractères).
    message : TextField
        Contenu du message (facultatif, champ texte).
    """
    name = models.CharField(max_length=100, null=False)  # Nom du contact (obligatoire).
    mail = models.CharField(max_length=250, null=False)  # Adresse e-mail (obligatoire).
    subject = models.CharField(max_length=100)  # Sujet du message (facultatif).
    message = models.TextField(null=True)  # Contenu du message (facultatif).