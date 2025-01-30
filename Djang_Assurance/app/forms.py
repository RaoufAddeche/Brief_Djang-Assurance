from django import forms
from .models import Reg_model, Prediction
from django.db.utils import OperationalError

class PredictionForm(forms.ModelForm):
    """
    Formulaire pour le personnel afin de créer un objet Prediction.

    Ce formulaire exclut certains champs :
    - 'result' : Ce champ est calculé dynamiquement et ne doit pas être défini manuellement.
    - 'made_by_staff' et 'made_by' : Ces champs sont définis automatiquement en fonction de l'utilisateur.
    """
    class Meta:
        model = Prediction
        fields = '__all__'
        exclude = ['result', 'made_by_staff', 'made_by']

    def clean(self):
        """
        Nettoie et valide les données du formulaire.

        Si le champ 'sex' contient 'homme' ou 'femme', les valeurs des champs
        'sex', 'smoker' et 'region' sont transformées en anglais à l'aide de la méthode
        `en_transform` de l'objet Prediction.
        """
        cleaned_data = super().clean()
        if cleaned_data["sex"] in {'homme', 'femme'}:
            # Création temporaire d'une instance Prediction pour appliquer les transformations
            prediction = Prediction(**cleaned_data)
            prediction.en_transform()  # Transformation des champs en anglais

            # Mise à jour des données nettoyées
            cleaned_data["sex"] = prediction.sex
            cleaned_data["smoker"] = prediction.smoker
            cleaned_data["region"] = prediction.region
            return cleaned_data
        else:
            return cleaned_data


class UserPredictionForm(forms.ModelForm):
    """
    Formulaire pour les utilisateurs afin de créer un objet Prediction.

    Ce formulaire exclut certains champs :
    - 'result' : Ce champ est calculé dynamiquement.
    - 'reg_model' : Le modèle de régression est défini par défaut comme null pour choisir
      la prédiction la plus coûteuse parmi tous les modèles.
    - 'user_id', 'made_by', 'made_by_staff' : Ces champs sont définis automatiquement.
    """
    class Meta:
        model = Prediction
        fields = '__all__'
        exclude = ['result', 'made_by_staff', 'reg_model', 'user_id', 'made_by']

    def clean(self):
        """
        Nettoie et valide les données du formulaire.

        Si le champ 'sex' contient 'homme' ou 'femme', les valeurs des champs
        'sex', 'smoker' et 'region' sont transformées en anglais à l'aide de la méthode
        `en_transform` de l'objet Prediction.
        """
        cleaned_data = super().clean()
        if cleaned_data["sex"] in {'homme', 'femme'}:
            # Création temporaire d'une instance Prediction pour appliquer les transformations
            prediction = Prediction(**cleaned_data)
            prediction.en_transform()  # Transformation des champs en anglais

            # Mise à jour des données nettoyées
            cleaned_data["sex"] = prediction.sex
            cleaned_data["smoker"] = prediction.smoker
            cleaned_data["region"] = prediction.region
            return cleaned_data
        else:
            return cleaned_data


class PredictionFilterForm(forms.Form):
    """
    Formulaire pour rechercher et filtrer les prédictions.

    Ce formulaire permet de filtrer les prédictions en fonction de plusieurs critères,
    comme l'âge, le poids, le genre, le statut de fumeur, la région, etc.
    """

    def __init__(self, *args, **kwargs):
        """
        Initialise le formulaire et charge dynamiquement les choix pour le champ 'reg_model'.

        Si la table Reg_model n'existe pas encore (par exemple, lors de la première migration),
        le champ 'reg_model' est laissé vide pour éviter les erreurs.
        """
        super().__init__(*args, **kwargs)
        try:
            # Charge dynamiquement les choix de modèles de régression
            reg_models = Reg_model.objects.all()
            self.fields['reg_model'].choices = [("", "Tous")] + [(model.name, model.name) for model in reg_models]
        except OperationalError:
            # Si la table n'existe pas encore, on laisse le champ vide
            self.fields['reg_model'].choices = [("", "Tous")]

    # Champs pour filtrer les prédictions
    user = forms.CharField(required=False, label="Nom d'utilisateur")
    min_age = forms.IntegerField(required=False, min_value=0, max_value=200, label="Âge minimum")
    max_age = forms.IntegerField(required=False, min_value=0, max_value=200, label="Âge maximum")
    min_children = forms.IntegerField(required=False, min_value=0, max_value=20, label="Nombre minimum d'enfants")
    max_children = forms.IntegerField(required=False, min_value=0, max_value=20, label="Nombre maximum d'enfants")
    min_weight = forms.FloatField(required=False, min_value=0, max_value=300, label="Poids minimum (kg)")
    max_weight = forms.FloatField(required=False, min_value=0, max_value=300, label="Poids maximum (kg)")
    min_size = forms.FloatField(required=False, min_value=0, max_value=300, label="Taille minimum (cm)")
    max_size = forms.FloatField(required=False, min_value=0, max_value=300, label="Taille maximum (cm)")
    sex = forms.ChoiceField(
        required=False,
        choices=[("", "Tous"), ('femme', 'femme'), ('homme', 'homme')],
        label="Genre"
    )
    smoker = forms.ChoiceField(
        required=False,
        choices=[("", "Tous"), ('oui', 'oui'), ('non', 'non')],
        label="Fumeur"
    )
    region = forms.ChoiceField(
        required=False,
        choices=[
            ("", "Toutes"),
            ("Sud Est", "Sud Est"),
            ("Sud Ouest", "Sud Ouest"),
            ("Nord Ouest", "Nord Ouest"),
            ("Nord Est", "Nord Est")
        ],
        label="Région"
    )
    reg_model = forms.ChoiceField(
        required=False,
        choices=[],
        label="Modèle"
    )
    sort_by = forms.ChoiceField(
        required=False,
        choices=[
            ("age", "Âge"),
            ("weight", "Poids"),
            ("size", "Taille"),
            ("result", "Résultat"),
        ],
        label="Trier par",
    )
    order = forms.ChoiceField(
        required=False,
        choices=[("asc", "Ascendant"), ("desc", "Descendant")],
        label="Ordre",
    )