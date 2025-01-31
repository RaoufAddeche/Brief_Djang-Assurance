# Djang Assurance

![image](Djang_Assurance/staticfiles/css/dist/logo.jpg)

## Description

**Djang Assurance** est une application web développée avec le framework Django pour répondre à un appel d'offre d'Assur'AImant, un assureur français souhaitant s'implanter aux États-Unis. L'application utilise des modèles de Machine Learning pour estimer le montant des redevances d'assurance en fonction de plusieurs paramètres. Elle propose une interface complète pour les utilisateurs, les courtiers, et inclut des fonctionnalités de gestion de rendez-vous, d'informations, et de personnalisation du thème.

---

## Fonctionnalités

### 1. Application de prédictions
- **Prédictions pour les utilisateurs** :
  - Estimation du montant des redevances en fonction des données saisies.
  - Modification des informations et affichage des résultats.

- **Prédictions pour les courtiers** :
  - Estimations pour plusieurs adhérents.
  - Historique des prédictions avec filtres.
  - Choix du modèle de prédiction.

### 2. Application users
- **Class Customers** :
  - Inscription.
  - Aperçu et modification du profil.

- **Class Staff** :
  - Aperçu et modification du profil.

### 3. Application meetings
- Gestion des rendez-vous :
  - Visualisation du planning.
  - Réservation de créneaux.
  - Restrictions pour éviter les doublons.

### 4. Application infos
- Pages informatives :
  - `News` : Dernières actualités.
  - `About us` : Présentation de l'entreprise.
  - `Privacy Policy` : Politique de confidentialité.
  - `Contact` : Formulaire de contact.

### 5. Application theme
- Gestion du front-end avec **django-tailwind**.

---

## Modèle de Machine Learning

L'application repose sur un modèle de **régression** pour estimer le montant des redevances d'assurance. Les paramètres pris en compte sont :
- 🏷 **Âge de l'assuré**  
- ❤️ **Genre de l'assuré** (données anonymisées)  
- 🚬 **Consommation de tabac**  
- 📍 **Zone géographique**  
- 📏 **Poids et taille**  
- 👶 **Nombre d'enfants**  

Le modèle est entraîné sur des données historiques des clients d'Assur'AImant et est régulièrement mis à jour via un **pipeline d'entraînement automatique**.

---

## Structure du Projet

| Fichier/Dossier              | Description                                                                 |
|------------------------------|-----------------------------------------------------------------------------|
| `Djang_Assurance/`           | Dossier principal du projet contenant les settings et les chemins.          |
| `Djang_Assurance/app/`       | Applications pour les prédictions des utilisateurs et du staff.             |
| `Djang_Assurance/infos/`     | Templates pour les pages informatives du site.                              |
| `Djang_Assurance/meetings/`  | Gestion des réservations et du planning.                                    |
| `Djang_Assurance/staticfiles/` | Médias, classes CSS et fichiers JS.                                       |
| `Djang_Assurance/theme/`     | Gestion du front-end (template de base, header, footer).                    |
| `Djang_Assurance/user/`      | Gestion des classes Users et Staff, inscription et connexion.               |
| `Djang_Assurance/db.sqlite3` | Base de données SQLite contenant les tables (users, staff, meetings, etc.). |
| `requirements.txt`           | Liste des dépendances Python nécessaires pour le projet.                    |
| `manage.py`                  | Fichier de configuration et d'exécution du projet.                         |
| `bricospider.csv`            | Données brutes scrappées au format CSV.                                     |
| `.gitignore`                 | Liste des fichiers et dossiers à ignorer par Git.                          |

---

## Installation et Utilisation

### Prérequis
- Python 3.8+

### Étapes d’installation

1. Clonez le dépôt Git :
   ```bash
   git clone git@github.com:RaoufAddeche/Brief_Djang-Assurance.git
        ```

## Contribution

Les contributions sont les bienvenues ! Veuillez suivre les étapes suivantes :

    Forkez le dépôt.
    Créez une branche pour vos modifications : git checkout -b feature/ma-fonctionnalite.
    Commitez vos changements : git commit -m "Ajout d'une nouvelle fonctionnalité".
    Poussez vos modifications : git push origin feature/ma-fonctionnalite.
    Ouvrez une Pull Request.

## Licence

Ce projet est sous licence MIT. Consultez le fichier LICENSE pour plus d'informations.
Auteurs

    Unicorn Power - Équipe de développement full-stack.
    Contact : email@example.com

## Remerciements

Merci à Assur'AImant pour leur confiance et à tous les contributeurs ayant participé au développement de ce projet.
