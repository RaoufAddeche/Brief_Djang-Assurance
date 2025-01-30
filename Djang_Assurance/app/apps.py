from django.apps import AppConfig


class AppConfig(AppConfig):
    """
    Classe de configuration pour l'application Django.

    Attributs :
    -----------
    default_auto_field : str
        Définit le type de champ par défaut pour les clés primaires des modèles.
        Ici, 'django.db.models.BigAutoField' est utilisé, ce qui correspond à un entier 64 bits.
    name : str
        Nom de l'application. Ici, l'application est nommée 'app'.

    Méthodes :
    ----------
    ready() :
        Méthode appelée lorsque l'application est prête. Elle est utilisée ici pour
        importer les signaux définis dans 'app.signals'.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app'

    def ready(self):
        """
        Méthode appelée lorsque l'application est entièrement chargée.

        Cette méthode importe le module 'app.signals' pour enregistrer les gestionnaires
        de signaux. Cela garantit que les signaux sont connectés et prêts à être utilisés
        lorsque l'application est en cours d'exécution.
        """
        # Importation des signaux définis dans le fichier 'app/signals.py'.
        # Cela permet de connecter les gestionnaires de signaux à leurs événements.
        import app.signals