from django.db.models.signals import post_migrate
from django.dispatch import receiver
from user.models import CustomUser, StaffUser
from .models import Reg_model, Prediction
from meetings.models import Appointment, Availability
from datetime import date, time


@receiver(post_migrate)
def after_migrations(sender, **kwargs):
    """
    Signal exécuté après les migrations pour initialiser les données de base.

    Ce signal crée :
    - Des modèles de régression (`Reg_model`) pour les prédictions.
    - Des utilisateurs (`CustomUser`) et des utilisateurs staff (`StaffUser`).
    - Des prédictions (`Prediction`) associées aux utilisateurs.
    - Des rendez-vous (`Appointment`) pour les utilisateurs et les conseillers.

    Paramètres :
    ------------
    sender : AppConfig
        L'application qui a déclenché le signal.
    kwargs : dict
        Arguments supplémentaires passés au signal.
    """
    if not Reg_model.objects.all():
        # Initialisation des modèles de régression
        print("Initialisation des modèles...")
        reg1 = Reg_model.objects.create(
            name="linéaire basique", path="app/regression/models/basic_linreg_model.pkl"
        )
        reg2 = Reg_model.objects.create(
            name="Gradient boosting", path="app/regression/models/gb_model.pkl"
        )
        reg3 = Reg_model.objects.create(
            name="linéaire", path="app/regression/models/linreg_model.pkl"
        )
        reg4 = Reg_model.objects.create(
            name="random forest", path="app/regression/models/rf_model.pkl"
        )
        reg5 = Reg_model.objects.create(
            name="ridge_model", path="app/regression/models/ridge_model.pkl"
        )
        reg6 = Reg_model.objects.create(
            name="lasso model", path="app/regression/models/best_lasso_model.pkl"
        )

        # Initialisation des utilisateurs
        print("Initialisation des utilisateurs...")
        user1 = CustomUser.objects.create_user(
            username="JeanMichou",
            prenom="Jean",
            nom="Michou",
            password="password",
            age=72,
            adresse="2 rue de la corne",
            email="qqsdsd@sd.fr",
        )
        user2 = CustomUser.objects.create_user(
            username="gisèle",
            prenom="gis",
            nom="elle",
            password="password",
            age=19,
            adresse="37 rue de la licorne",
            email="qsd@sd.fr",
        )
        user3 = CustomUser.objects.create_user(
            username="ludivine",
            prenom="Lu",
            nom="Divine",
            password="password",
            is_staff=True,
        )
        user5 = CustomUser.objects.create_user(
            username="raouf", prenom="Ra", nom="Ouf", password="password", is_staff=True
        )
        user4 = CustomUser.objects.create_user(
            username="vic", prenom="vic", nom="tor", password="password", is_staff=True
        )

        print("Initialisation des staffusers...")
        # Création des utilisateurs staff (StaffUser) associés
        staff1, _ = StaffUser.objects.get_or_create(user=user3)
        staff1.img = "css/dist/ludi_licorne.jpg"
        staff1.description = (
            "Toujours rapide et efficace, Lu Divine est la conseillère idéale pour ceux qui veulent des réponses claires "
            "et précises sans perdre une minute. Son grand cœur et son approche bienveillante font d’elle une véritable alliée "
            "pour ses clients. Et en plus de son expertise en assurance, elle est une véritable as de la mécanique !"
        )
        staff1.title = "Conseillère en Assurance - Lu Divine"
        staff1.save()

        staff2, _ = StaffUser.objects.get_or_create(user=user4)
        staff2.img = "css/dist/vic_licorne.jpg"
        staff2.description = (
            "Un brin tête en l'air mais débordante d’énergie positive, Vi Tor met des paillettes partout où elle passe ! "
            "Avec elle, même les démarches administratives deviennent plus fun et légères. Spécialiste en assurance et passionnée "
            "de maquillage, elle saura non seulement vous conseiller sur vos contrats mais aussi vous donner des astuces beauté."
        )
        staff2.title = "Conseillère en Assurance - Vi Tor"
        staff2.save()

        staff3, _ = StaffUser.objects.get_or_create(user=user5)
        staff3.img = "css/dist/raouf_licorne.jpg"
        staff3.description = (
            "Ra Ouf est le conseiller en assurance qui trouve toujours une solution. Son assurance inébranlable et son sang-froid "
            "légendaire font de lui un roc sur lequel ses clients peuvent compter. Peu importe l’obstacle, il est là pour le surmonter "
            "et vous guider en toute sérénité."
        )
        staff3.title = "Conseiller en Assurance - Ra Ouf"
        staff3.save()

        # Initialisation des prédictions
        print("Initialisation des prédictions...")
        pred_list = []
        pred_list.append(
            Prediction.objects.create(
                user_id=user1,
                made_by=user3,
                age=30,
                reg_model=reg1,
                children=2,
                weight=70.5,
                size=170,
                smoker="no",
                region="southwest",
            )
        )
        pred_list.append(
            Prediction.objects.create(
                user_id=user2,
                made_by=user3,
                age=40,
                reg_model=reg2,
                children=1,
                weight=80.2,
                size=175,
                smoker="yes",
                region="northeast",
            )
        )
        pred_list.append(
            Prediction.objects.create(
                user_id=user2,
                made_by=user4,
                age=50,
                reg_model=reg3,
                children=0,
                weight=90.2,
                size=165,
                smoker="yes",
                region="southeast",
            )
        )
        pred_list.append(
            Prediction.objects.create(
                user_id=user1,
                made_by=user3,
                age=45,
                reg_model=reg4,
                children=4,
                weight=103,
                size=197,
                smoker="no",
                region="southwest",
            )
        )
        pred_list.append(
            Prediction.objects.create(
                user_id=user2,
                made_by=user3,
                age=70,
                reg_model=reg5,
                children=3,
                weight=150,
                size=145,
                smoker="no",
                region="northeast",
            )
        )
        pred_list.append(
            Prediction.objects.create(
                user_id=user1,
                made_by=user4,
                age=55,
                reg_model=reg6,
                children=5,
                weight=45,
                size=160,
                smoker="yes",
                region="southeast",
            )
        )
        for pred in pred_list:
            pred.pred()  # Calculer le résultat de la prédiction.
            pred.fr_transform()  # Localiser certains champs (ex. : sexe, fumeur).
            pred.save()

        # Initialisation des rendez-vous
        print("Initialisation des rendez-vous...")
        Appointment.objects.create(
            user=user1,
            staff_user=staff2,
            date=date(2025, 1, 30),
            start_time=time(14, 0),
            end_time=time(15, 0),
        )
        Appointment.objects.create(
            user=user1,
            staff_user=staff1,
            date=date(2025, 1, 30),
            start_time=time(13, 0),
            end_time=time(14, 0),
        )
        Appointment.objects.create(
            user=user1,
            staff_user=staff3,
            date=date(2025, 1, 30),
            start_time=time(15, 0),
            end_time=time(16, 0),
        )
        print("Données initialisées avec succès !")
