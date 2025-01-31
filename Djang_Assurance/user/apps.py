from django.apps import AppConfig


class UserConfig(AppConfig):
    """
    Configuration de l'application 'user'.

    Attributs :
    -----------
    default_auto_field : str
        Type de champ auto-incrémenté par défaut pour les modèles (BigAutoField).
    name : str
        Nom de l'application (doit correspondre au nom du dossier contenant l'application).

    Méthodes :
    ----------
    ready():
        Méthode appelée lorsque l'application est prête. Utilisée ici pour importer les signaux.
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "user"

    def ready(self):
        """
        Importation des signaux de l'application 'user' lors de son initialisation.
        """
        import user.signals
