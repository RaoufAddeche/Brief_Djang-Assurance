from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic.edit import FormView, UpdateView
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import InscriptionForm, ModifProfilForm
from django.views import View
from .models import CustomUser


class RedirectionView(LoginRequiredMixin, View):
    """
    Vue pour rediriger l'utilisateur après connexion en fonction de son rôle.

    Méthodes :
    ----------
    get(request, *args, **kwargs):
        Redirige les utilisateurs staff vers "prediction" et les autres vers "user_prediction".
    """
    def get(self, request, *args, **kwargs):
        if request.user.is_staff:
            return redirect("prediction")
        else:
            return redirect("user_prediction")


class InscriptionView(FormView):
    """
    Vue pour gérer l'inscription des utilisateurs.

    Attributs :
    -----------
    template_name : str
        Chemin vers le template d'inscription.
    form_class : Form
        Formulaire utilisé pour l'inscription.
    success_url : str
        URL de redirection après une inscription réussie.

    Méthodes :
    ----------
    form_valid(form):
        Sauvegarde l'utilisateur et affiche un message de succès.
    form_invalid(form):
        Affiche un message d'erreur si le formulaire est invalide.
    """
    template_name = "user/inscription.html"
    form_class = InscriptionForm
    success_url = reverse_lazy("connexion")

    def form_valid(self, form):
        # Sauvegarde de l'utilisateur
        utilisateur = form.save(commit=False)
        utilisateur.first_name = form.cleaned_data["prenom"]
        utilisateur.last_name = form.cleaned_data["nom"]
        utilisateur.set_password(form.cleaned_data["mot_de_passe"])
        utilisateur.save()

        # Succès
        messages.success(
            self.request, "Inscription réussie ! Vous pouvez maintenant vous connecter."
        )
        return super().form_valid(form)

    def form_invalid(self, form):
        # Erreur
        messages.error(self.request, "Veuillez corriger les erreurs du formulaire.")
        return super().form_invalid(form)


class Connexion(LoginView):
    """
    Vue pour gérer la connexion des utilisateurs.

    Attributs :
    -----------
    template_name : str
        Chemin vers le template de connexion.
    redirect_authenticated_user : bool
        Redirige les utilisateurs déjà connectés.

    Méthodes :
    ----------
    form_invalid(form):
        Affiche un message d'erreur si les informations de connexion sont incorrectes.
    """
    template_name = "user/connexion.html"
    redirect_authenticated_user = True

    def form_invalid(self, form):
        messages.error(
            self.request,
            "Nom d'utilisateur ou mot de passe incorrect. Veuillez réessayer.",
        )
        return super().form_invalid(form)


class DeconnexionView(LogoutView):
    """
    Vue pour gérer la déconnexion des utilisateurs.

    Attributs :
    -----------
    next_page : str
        URL de redirection après la déconnexion.
    """
    next_page = reverse_lazy("accueil")


class Accueil(TemplateView):
    """
    Vue pour afficher la page d'accueil.

    Attributs :
    -----------
    template_name : str
        Chemin vers le template de la page d'accueil.

    Méthodes :
    ----------
    get_context_data(**kwargs):
        Ajoute l'utilisateur connecté au contexte.
    """
    template_name = "user/accueil.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user"] = self.request.user
        return context


class ProfilView(LoginRequiredMixin, TemplateView):
    """
    Vue pour afficher le profil de l'utilisateur connecté.

    Attributs :
    -----------
    template_name : str
        Chemin vers le template du profil.

    Méthodes :
    ----------
    get_context_data(**kwargs):
        Ajoute l'utilisateur connecté au contexte.
    """
    template_name = "user/profil.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user"] = self.request.user
        return context


class ModifProfilView(LoginRequiredMixin, UpdateView):
    """
    Vue pour permettre à l'utilisateur de modifier son profil.

    Attributs :
    -----------
    model : Model
        Modèle associé à la vue (CustomUser).
    form_class : Form
        Formulaire utilisé pour la modification du profil.
    template_name : str
        Chemin vers le template de modification du profil.
    success_url : str
        URL de redirection après une modification réussie.

    Méthodes :
    ----------
    get_object():
        Retourne l'utilisateur connecté.
    """
    model = CustomUser
    form_class = ModifProfilForm
    template_name = "user/modif_profil.html"
    success_url = reverse_lazy("accueil")

    def get_object(self):
        return self.request.user


class SuppressionUser(LoginRequiredMixin, View):
    """
    Vue pour gérer la suppression du compte utilisateur.

    Attributs :
    -----------
    template_name : str
        Chemin vers le template de confirmation de suppression.

    Méthodes :
    ----------
    get(request, *args, **kwargs):
        Affiche la page de confirmation de suppression.
    post(request, *args, **kwargs):
        Supprime le compte utilisateur et redirige vers la page d'accueil.
    """
    template_name = "user/suppression_compte.html"

    def get(self, request, *args, **kwargs):
        # Afficher la page de confirmation
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        user = request.user
        user.delete()
        messages.success(request, "Votre compte a été supprimé avec succès.")
        return redirect("accueil")