from django.views.generic import TemplateView, FormView
from .forms import ContactForm
from django.contrib import messages
from django.urls import reverse_lazy

# Définition des vues ici.


class NewsView(TemplateView):
    """
    Vue pour afficher la page des actualités.

    Attributs :
    -----------
    template_name : str
        Chemin vers le template utilisé pour afficher la page.
    """
    template_name = 'infos/news.html'  # Template pour la page des actualités.


class AboutView(TemplateView):
    """
    Vue pour afficher la page "À propos".

    Attributs :
    -----------
    template_name : str
        Chemin vers le template utilisé pour afficher la page.
    """
    template_name = 'infos/about.html'  # Template pour la page "À propos".


class PrivacyView(TemplateView):
    """
    Vue pour afficher la page de politique de confidentialité.

    Attributs :
    -----------
    template_name : str
        Chemin vers le template utilisé pour afficher la page.
    """
    template_name = 'infos/privacy.html'  # Template pour la page de politique de confidentialité.


class ContactView(FormView):
    """
    Vue pour gérer le formulaire de contact.

    Attributs :
    -----------
    template_name : str
        Chemin vers le template utilisé pour afficher le formulaire de contact.
    form_class : ContactForm
        Classe de formulaire utilisée pour collecter les données de contact.
    success_url : str
        URL vers laquelle rediriger après la soumission réussie du formulaire.
    """
    template_name = 'infos/contact.html'  # Template pour la page de contact.
    form_class = ContactForm  # Formulaire utilisé pour collecter les données de contact.
    success_url = reverse_lazy('contact')  # Redirection après soumission réussie.

    def form_valid(self, form):
        """
        Traite le formulaire après validation :
        - Enregistre les données du formulaire dans la base de données.
        - Affiche un message de succès à l'utilisateur.

        Paramètres :
        ------------
        form : ContactForm
            Instance du formulaire validé.

        Retourne :
        ---------
        HttpResponseRedirect
            Redirection vers l'URL de succès.
        """
        form.save()  # Enregistre les données du formulaire.
        # Ajoute un message de succès pour informer l'utilisateur.
        messages.success(self.request, "Votre message a bien été envoyé. Merci de nous avoir contactés !")
        return super().form_valid(form)  # Appelle la méthode parente pour gérer la redirection.