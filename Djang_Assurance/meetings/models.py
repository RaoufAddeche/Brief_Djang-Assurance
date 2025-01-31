from django.db import models
from user.models import StaffUser, CustomUser


class Availability(models.Model):
    """
    Modèle représentant les disponibilités d'un membre du personnel.

    Attributs :
    -----------
    DAYS_OF_WEEK : list
        Liste des jours de la semaine avec leurs valeurs numériques (0 = lundi, 6 = dimanche).
    staff_user : ForeignKey
        Référence au membre du personnel (StaffUser) associé à cette disponibilité.
    day_of_week : IntegerField
        Jour de la semaine (0 = lundi, 6 = dimanche).
    start_time : TimeField
        Heure de début de la disponibilité (exemple : 13:00).
    end_time : TimeField
        Heure de fin de la disponibilité (exemple : 16:00).

    Méta :
    ------
    unique_together : tuple
        Garantit qu'une combinaison unique de `staff_user`, `day_of_week`, `start_time` et `end_time` existe.

    Méthodes :
    ----------
    __str__():
        Retourne une représentation lisible de la disponibilité (jour et plage horaire).
    """

    DAYS_OF_WEEK = [
        (0, "Monday"),
        (1, "Tuesday"),
        (2, "Wednesday"),
        (3, "Thursday"),
        (4, "Friday"),
        (5, "Saturday"),
        (6, "Sunday"),
    ]

    staff_user = models.ForeignKey(
        StaffUser, on_delete=models.CASCADE, related_name="availabilities"
    )  # Membre du personnel associé à cette disponibilité.
    day_of_week = models.IntegerField(
        choices=DAYS_OF_WEEK
    )  # Jour de la semaine (exemple : 0 = lundi).
    start_time = (
        models.TimeField()
    )  # Heure de début de la disponibilité (exemple : 13:00).
    end_time = models.TimeField()  # Heure de fin de la disponibilité (exemple : 16:00).

    class Meta:
        unique_together = (
            "staff_user",
            "day_of_week",
            "start_time",
            "end_time",
        )  # Contrainte d'unicité.

    def __str__(self):
        """
        Retourne une chaîne lisible représentant la disponibilité.
        Exemple : "Monday 13:00 - 16:00".
        """
        return f"{self.get_day_of_week_display()} {self.start_time} - {self.end_time}"


class Appointment(models.Model):
    """
    Modèle représentant un rendez-vous entre un utilisateur et un membre du personnel.

    Attributs :
    -----------
    user : ForeignKey
        Référence à l'utilisateur (CustomUser) qui prend le rendez-vous.
    staff_user : ForeignKey
        Référence au membre du personnel (StaffUser) concerné par le rendez-vous.
    date : DateField
        Date du rendez-vous.
    start_time : TimeField
        Heure de début du rendez-vous.
    end_time : TimeField
        Heure de fin du rendez-vous.

    Méta :
    ------
    unique_together : tuple
        Garantit qu'une combinaison unique de `staff_user`, `date`, `start_time` et `end_time` existe.

    Méthodes :
    ----------
    __str__():
        Retourne une représentation lisible du rendez-vous (membre du personnel, date et plage horaire).
    clean():
        Vérifie si le rendez-vous respecte les disponibilités du membre du personnel.
    """

    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="appointments"
    )  # Utilisateur qui prend le rendez-vous.
    staff_user = models.ForeignKey(
        StaffUser, on_delete=models.CASCADE, related_name="appointments_with_staff"
    )  # Membre du personnel concerné par le rendez-vous.
    date = models.DateField()  # Date du rendez-vous.
    start_time = models.TimeField()  # Heure de début du rendez-vous.
    end_time = models.TimeField()  # Heure de fin du rendez-vous.

    class Meta:
        unique_together = (
            "staff_user",
            "date",
            "start_time",
            "end_time",
        )  # Contrainte d'unicité.

    def __str__(self):
        """
        Retourne une chaîne lisible représentant le rendez-vous.
        Exemple : "Appointment with John Doe on 2025-01-30 from 13:00 to 14:00".
        """
        return f"Appointment with {self.staff_user.user} on {self.date} from {self.start_time} to {self.end_time}"

    def clean(self):
        """
        Vérifie si le rendez-vous respecte les disponibilités du membre du personnel.

        Lève une ValidationError si :
        - Le rendez-vous est en dehors des plages de disponibilité du membre du personnel.

        Exceptions :
        ------------
        ValidationError :
            Si le rendez-vous ne correspond pas aux disponibilités du membre du personnel.
        """
        from django.core.exceptions import ValidationError

        # Recherche une disponibilité correspondant au jour, à l'heure de début et à l'heure de fin.
        availability = Availability.objects.filter(
            staff_user=self.staff_user,
            day_of_week=self.date.weekday(),  # Convertit la date en jour de la semaine (0 = lundi).
            start_time__lte=self.start_time,  # Vérifie que l'heure de début est dans la plage.
            end_time__gte=self.end_time,  # Vérifie que l'heure de fin est dans la plage.
        )
        if not availability.exists():
            # Lève une erreur si aucune disponibilité ne correspond.
            raise ValidationError(
                "This appointment is outside the staff user's availability."
            )
