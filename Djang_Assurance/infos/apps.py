from django.apps import AppConfig


class InfosConfig(AppConfig):
    """
    Configuration de l'application 'infos'.

    Attributs :
    -----------
    default_auto_field : str
        Définit le type de clé primaire par défaut pour les modèles de l'application.
    name : str
        Nom de l'application (doit correspondre au nom du dossier contenant l'application).
    """
    default_auto_field = 'django.db.models.BigAutoField'  # Utilise un champ auto-incrémenté pour les clés primaires.
    name = 'infos'  # Nom de l'application.