from django import template
from datetime import datetime

# Enregistrement de la bibliothèque de filtres personnalisés
register = template.Library()

@register.filter
def get_item(dictionary, key):
    """
    Accède à un élément dans un dictionnaire par sa clé.

    Paramètres :
    ------------
    dictionary : dict
        Le dictionnaire dans lequel chercher l'élément.
    key : str
        La clé de l'élément à récupérer.

    Retourne :
    ---------
    object
        La valeur associée à la clé dans le dictionnaire, ou None si la clé n'existe pas.
    """
    return dictionary.get(key)  # Retourne la valeur associée à la clé.


@register.filter
def availability_for_day_hour(availabilities, date_hour):
    """
    Vérifie si une disponibilité existe pour une date et une heure spécifiques.

    Paramètres :
    ------------
    availabilities : list
        Liste des objets de disponibilité (chaque objet doit avoir `day_of_week`, `start_time` et `end_time`).
    date_hour : str
        Chaîne contenant la date et l'heure au format "YYYY-MM-DD|HH:MM".

    Retourne :
    ---------
    bool
        True si une disponibilité correspond à la date et l'heure spécifiées, sinon False.
    """
    # Sépare la date et l'heure à partir de la chaîne d'entrée
    date, hour = date_hour.split('|')
    for availability in availabilities:
        # Convertir la date pour obtenir le jour de la semaine (0 = lundi, 6 = dimanche)
        if availability.day_of_week == datetime.strptime(date, "%Y-%m-%d").weekday():
            # Convertir les heures de début et de fin en chaînes pour comparaison
            start_time = availability.start_time.strftime("%H:%M")
            end_time = availability.end_time.strftime("%H:%M")
            # Vérifie si l'heure donnée est dans l'intervalle de disponibilité
            if start_time <= hour < end_time:
                return True
    return False  # Retourne False si aucune disponibilité ne correspond.