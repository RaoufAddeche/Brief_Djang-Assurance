from django import forms
from .models import CustomUser


class InscriptionForm(forms.ModelForm):
    """
    Formulaire d'inscription pour les nouveaux utilisateurs.

    Champs :
    --------
    mot_de_passe : CharField
        Champ pour saisir le mot de passe avec un widget de type PasswordInput.

    Meta :
    ------
    model : CustomUser
        Modèle associé au formulaire.
    fields : list
        Liste des champs inclus dans le formulaire.
    labels : dict
        Étiquettes personnalisées pour les champs du formulaire.
    """

    mot_de_passe = forms.CharField(widget=forms.PasswordInput, label="Mot de passe")

    class Meta:
        model = CustomUser
        fields = [
            "email",
            "prenom",
            "nom",
            "mot_de_passe",
            "username",
            "age",
            "adresse",
        ]
        labels = {
            "username": "Nom d'utilisateur",
            "email": "Adresse e-mail",
            "age": "Âge",
            "adresse": "Adresse physique",
        }


class ModifProfilForm(forms.ModelForm):
    """
    Formulaire pour modifier le profil d'un utilisateur existant.

    Meta :
    ------
    model : CustomUser
        Modèle associé au formulaire.
    fields : list
        Liste des champs inclus dans le formulaire.
    """

    class Meta:
        model = CustomUser
        fields = ["prenom", "nom", "email", "age", "adresse"]
