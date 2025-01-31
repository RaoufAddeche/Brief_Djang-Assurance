from django.db import models
from user.models import CustomUser
from django.core.validators import MinValueValidator, MaxValueValidator
import pandas as pd
import cloudpickle

# Définition des choix pour les champs de type `CharField`
SEX_CHOICES = (("female", "Femme"), ("male", "Homme"))

SMOKER_CHOICES = (("yes", "Oui"), ("no", "Non"))

REGION_CHOICES = (
    ("southeast", "Sud Est"),
    ("southwest", "Sud Ouest"),
    ("northeast", "Nord Est"),
    ("northwest", "Nord Ouest"),
)


class Reg_model(models.Model):
    """
    Représente un modèle de régression utilisé pour les prédictions d'assurance.

    Attributs :
    -----------
    name : str
        Nom du modèle de régression (exemple : 'Lasso Regression Model').
    path : FilePathField
        Chemin vers le fichier sérialisé contenant le modèle de régression.
    """

    name = models.CharField(
        max_length=200,
        help_text="Le nom du modèle de régression (ex. : 'Lasso Regression Model').",
    )
    path = models.FilePathField(
        path="app/regression/models/",
        help_text="Le chemin vers le fichier sérialisé du modèle de régression.",
    )

    def calcul_prediction(self, age, sex, weight, size, children, smoker, region):
        """
        Calcule une prédiction d'assurance à l'aide du modèle de régression.

        Paramètres :
        ------------
        age : int
            Âge de l'utilisateur.
        sex : str
            Genre de l'utilisateur ('male' ou 'female').
        weight : float
            Poids de l'utilisateur en kilogrammes.
        size : float
            Taille de l'utilisateur en centimètres.
        children : int
            Nombre d'enfants de l'utilisateur.
        smoker : str
            Statut de fumeur de l'utilisateur ('yes' ou 'no').
        region : str
            Région de résidence de l'utilisateur.

        Retourne :
        ---------
        float
            La prime d'assurance prédite.
        """
        # Calcul de l'IMC (Indice de Masse Corporelle)
        bmi = weight / pow(size / 100, 2)
        # Création d'un DataFrame avec les données utilisateur
        data = pd.DataFrame(
            data=[[age, sex, bmi, children, smoker, region]],
            columns=["age", "sex", "bmi", "children", "smoker", "region"],
        )
        print(data)
        print(data.dtypes)
        # Chargement du modèle sérialisé
        with open(self.path, "rb") as f:
            reg = cloudpickle.load(f)
        # Prédiction à l'aide du modèle
        prediction = reg.predict(data)
        return prediction

    def __str__(self):
        return self.name


class Prediction(models.Model):
    """
    Représente une demande de prédiction d'un utilisateur et son résultat.

    Attributs :
    -----------
    age : int
        Âge de l'utilisateur (par défaut : 10).
    sex : str
        Genre de l'utilisateur ('male' ou 'female', par défaut : 'female').
    weight : float
        Poids de l'utilisateur en kilogrammes (par défaut : 60).
    size : float
        Taille de l'utilisateur en centimètres (par défaut : 170).
    children : int
        Nombre d'enfants de l'utilisateur (par défaut : 5).
    smoker : str
        Indique si l'utilisateur est fumeur ('yes' ou 'no', par défaut : 'no').
    region : str
        Région de résidence de l'utilisateur (par défaut : 'northwest').
    result : float
        Prime d'assurance prédite (nullable).
    user_id : ForeignKey
        Référence à l'utilisateur associé à la prédiction.
    reg_model : ForeignKey
        Modèle de régression utilisé pour la prédiction (nullable).
    made_by : ForeignKey
        Référence à l'utilisateur ayant effectué la prédiction.
    made_by_staff : bool
        Indique si la prédiction a été effectuée par un membre du personnel.
    """

    age = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(130)], default=10
    )
    sex = models.CharField(max_length=6, choices=SEX_CHOICES, default="female")
    weight = models.FloatField(
        validators=[MinValueValidator(1), MaxValueValidator(300)], default=60
    )
    size = models.FloatField(
        validators=[MinValueValidator(30), MaxValueValidator(300)], default=170
    )
    children = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(20)], default=5
    )
    smoker = models.CharField(max_length=3, choices=SMOKER_CHOICES, default="no")
    region = models.CharField(max_length=9, choices=REGION_CHOICES, default="northwest")
    result = models.FloatField(null=True)
    user_id = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, null=True, related_name="profile"
    )
    reg_model = models.ForeignKey(Reg_model, on_delete=models.SET_NULL, null=True)
    made_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    made_by_staff = models.BooleanField(default=False)

    def __str__(self):
        return f"Prédiction de l'utilisateur : {self.user_id} avec un résultat de : {self.result}"

    def pred(self):
        """
        Calcule la prime d'assurance à l'aide du modèle de régression spécifié ou
        choisit la prédiction la plus coûteuse parmi tous les modèles.

        Retourne :
        ---------
        None : Le résultat est stocké dans l'attribut `result`.
        """
        if self.made_by_staff:
            # Utilisation du modèle de régression spécifié
            pred = self.reg_model.calcul_prediction(
                self.age,
                self.sex,
                self.weight,
                self.size,
                self.children,
                self.smoker,
                self.region,
            )[0]
        else:
            # Si aucun modèle spécifique n'est choisi, on utilise la prédiction la plus coûteuse
            reg_models = Reg_model.objects.all()
            pred_list = []
            for model in reg_models:
                pred_list.append(
                    model.calcul_prediction(
                        self.age,
                        self.sex,
                        self.weight,
                        self.size,
                        self.children,
                        self.smoker,
                        self.region,
                    )[0]
                )
            pred_list.sort()
            pred = pred_list[-1]  # Choisir la prédiction la plus élevée
        self.result = round(pred, 2)

    def fr_transform(self):
        """
        Transforme les champs de la prédiction en leur équivalent français pour un affichage utilisateur.

        Transformations :
        - sex : 'male' -> 'homme', 'female' -> 'femme'
        - smoker : 'yes' -> 'oui', 'no' -> 'non'
        - region : Noms anglais -> Noms français
        """
        match self.sex:
            case "female":
                self.sex = "femme"
            case "male":
                self.sex = "homme"
        match self.smoker:
            case "yes":
                self.smoker = "oui"
            case "no":
                self.smoker = "non"
        match self.region:
            case "southeast":
                self.region = "Sud Est"
            case "southwest":
                self.region = "Sud Ouest"
            case "northeast":
                self.region = "Nord Est"
            case "northwest":
                self.region = "Nord Ouest"

    def en_transform(self):
        """
        Transforme les champs de la prédiction en leur équivalent anglais.

        Transformations :
        - sex : 'homme' -> 'male', 'femme' -> 'female'
        - smoker : 'oui' -> 'yes', 'non' -> 'no'
        - region : Noms français -> Noms anglais
        """
        match self.sex:
            case "femme":
                self.sex = "female"
            case "homme":
                self.sex = "male"
        match self.smoker:
            case "oui":
                self.smoker = "yes"
            case "non":
                self.smoker = "no"
        match self.region:
            case "Sud Est":
                self.region = "southeast"
            case "Sud Ouest":
                self.region = "southwest"
            case "Nord Est":
                self.region = "northeast"
            case "Nord Ouest":
                self.region = "northwest"
