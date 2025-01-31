from sklearn.base import BaseEstimator, TransformerMixin
import pandas as pd


class BmiTransformer(BaseEstimator, TransformerMixin):
    """
    Transformateur pour catégoriser l'indice de masse corporelle (IMC ou BMI en anglais).

    Paramètres :
    -----------
    columns : str
        Nom de la colonne contenant les valeurs de l'IMC à transformer.
    k : float, optionnel (par défaut 29.999)
        Seuil pour catégoriser l'IMC. Les valeurs inférieures à k seront dans la catégorie 0,
        et les valeurs supérieures ou égales à k seront dans la catégorie 1.

    Méthodes :
    ---------
    fit(X, y=None) :
        Méthode d'ajustement (ne fait rien ici car aucune opération d'apprentissage n'est nécessaire).
    transform(X0) :
        Transforme les données en ajoutant une colonne "bmi_category" avec les catégories d'IMC.
    """

    def __init__(self, columns=None, k=29.999):
        self.columns = columns
        self.k = k

    def fit(self, X, y=None):
        # Pas d'apprentissage nécessaire pour ce transformateur
        return self

    def transform(self, X0):
        """
        Transforme les données en ajoutant une colonne "bmi_category" basée sur les seuils définis.

        Paramètres :
        -----------
        X0 : array-like ou DataFrame
            Les données d'entrée contenant la colonne spécifiée.

        Retourne :
        ---------
        DataFrame
            Les données transformées avec une nouvelle colonne "bmi_category".
        """
        X = pd.DataFrame(X0)  # Conversion en DataFrame si nécessaire
        if self.columns == "bmi":
            # Définition des intervalles pour catégoriser l'IMC
            bins = [0, self.k, 100]
            labels = [0, 1]
            # Ajout de la colonne "bmi_category" avec les catégories
            X["bmi_category"] = pd.cut(X["bmi"], bins=bins, labels=labels, right=False)
        else:
            # Erreur si la colonne spécifiée n'est pas correcte
            raise ValueError("Vous devez spécifier les colonnes à transformer.")
        return X


class AgeTransformer(BaseEstimator, TransformerMixin):
    """
    Transformateur pour catégoriser l'âge.

    Paramètres :
    -----------
    columns : str
        Nom de la colonne contenant les valeurs d'âge à transformer.
    k : int, optionnel (par défaut 35)
        Seuil pour catégoriser l'âge. Les valeurs inférieures à k seront dans la catégorie 0,
        et les valeurs supérieures ou égales à k seront dans la catégorie 1.

    Méthodes :
    ---------
    fit(X, y=None) :
        Méthode d'ajustement (ne fait rien ici car aucune opération d'apprentissage n'est nécessaire).
    transform(X0) :
        Transforme les données en ajoutant une colonne "age_category" avec les catégories d'âge.
    """

    def __init__(self, columns=None, k=35):
        self.columns = columns
        self.k = k

    def fit(self, X, y=None):
        # Pas de calcul particulier nécessaire pour cette transformation
        return self

    def transform(self, X0):
        """
        Transforme les données en ajoutant une colonne "age_category" basée sur les seuils définis.

        Paramètres :
        -----------
        X0 : array-like ou DataFrame
            Les données d'entrée contenant la colonne spécifiée.

        Retourne :
        ---------
        DataFrame
            Les données transformées avec une nouvelle colonne "age_category".
        """
        X = pd.DataFrame(X0)  # Conversion en DataFrame si nécessaire
        if self.columns == "age":
            # Définition des intervalles pour catégoriser l'âge
            bins = [0, self.k, 100]  # Tranches d'âge
            labels = [0, 1]
            # Ajout de la colonne "age_category" avec les catégories
            X["age_category"] = pd.cut(X["age"], bins=bins, labels=labels, right=False)
        else:
            # Erreur si la colonne spécifiée n'est pas correcte
            raise ValueError("Vous devez spécifier les colonnes à transformer.")
        return X
