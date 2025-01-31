from django.db import models
from django.contrib.auth.models import AbstractUser

# Création de vos modèles ici.


class CustomUser(AbstractUser):
    """
    Modèle utilisateur personnalisé basé sur AbstractUser.

    Attributs :
    -----------
    prenom : CharField
        Prénom de l'utilisateur (obligatoire).
    nom : CharField
        Nom de l'utilisateur (obligatoire).
    age : PositiveIntegerField
        Âge de l'utilisateur (optionnel).
    adresse : TextField
        Adresse physique de l'utilisateur (optionnelle).
    """

    prenom = models.CharField(max_length=30, null=False)
    nom = models.CharField(max_length=30, null=False)
    age = models.PositiveIntegerField(null=True, blank=True)
    adresse = models.TextField(null=True, blank=True)


class StaffUser(models.Model):
    """
    Modèle représentant un membre du personnel.

    Attributs :
    -----------
    img : CharField
        URL ou chemin vers une image associée au membre du personnel (optionnel).
    user : OneToOneField
        Relation un-à-un avec le modèle CustomUser. Supprime le StaffUser si le CustomUser est supprimé.
    description : TextField
        Description du membre du personnel (optionnelle).
    title : CharField
        Titre ou poste du membre du personnel (optionnel).

    Meta :
    ------
    verbose_name : str
        Nom singulier affiché dans l'interface d'administration.
    verbose_name_plural : str
        Nom pluriel affiché dans l'interface d'administration.
    """

    img = models.CharField(max_length=255, null=True, blank=True)
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,  # Supprime le StaffUser si CustomUser est supprimé
        primary_key=True,  # Utilise le même ID que CustomUser
    )
    description = models.TextField(null=True)
    title = models.CharField(max_length=300, null=True)

    class Meta:
        verbose_name = "Staff User"
        verbose_name_plural = "Staff Users"
