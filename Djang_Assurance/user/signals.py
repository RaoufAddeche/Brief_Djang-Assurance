from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CustomUser, StaffUser


# Signal post-save pour créer automatiquement un StaffUser
@receiver(post_save, sender=CustomUser)
def create_staff_user(sender, instance, created, **kwargs):
    """
    Signal pour créer automatiquement un StaffUser lorsqu'un CustomUser avec le statut 'is_staff' est sauvegardé.

    Paramètres :
    ------------
    sender : Model
        Le modèle qui a déclenché le signal (ici, CustomUser).
    instance : CustomUser
        L'instance de CustomUser qui a été sauvegardée.
    created : bool
        Indique si l'instance a été créée (True) ou mise à jour (False).
    **kwargs : dict
        Arguments supplémentaires.

    Action :
    --------
    Si l'utilisateur est un membre du staff (is_staff=True), un StaffUser correspondant est créé
    automatiquement s'il n'existe pas déjà.
    """
    if instance.is_staff:
        # Vérifie si un StaffUser correspondant existe déjà
        StaffUser.objects.get_or_create(
            user=instance,  # Utilise le champ OneToOneField pour la liaison
            defaults={
                # Les champs supplémentaires peuvent être initialisés ici
            },
        )
