from django.apps import AppConfig


class MeetingsConfig(AppConfig):
    """
    Configuration de l'application 'meetings'.

    Attributs :
    -----------
    default_auto_field : str
        Définit le type de clé primaire par défaut pour les modèles de l'application.
    name : str
        Nom de l'application (doit correspondre au nom du dossier contenant l'application).

    Méthodes :
    ----------
    ready():
        Méthode appelée lorsque l'application est prête. Utilisée ici pour importer les signaux.
    """

    default_auto_field = "django.db.models.BigAutoField"  # Utilise un champ auto-incrémenté pour les clés primaires.
    name = "meetings"  # Nom de l'application.

    def ready(self):
        """
        Méthode appelée lorsque l'application est prête.

        Cette méthode importe le module `meetings.signals` pour enregistrer les gestionnaires de signaux.
        """
        import meetings.signals  # Importation des signaux pour connecter les gestionnaires.
