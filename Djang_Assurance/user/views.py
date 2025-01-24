from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic.edit import FormView
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import InscriptionForm


class InscriptionView(FormView):
    template_name= 'user/inscription.html'
    form_class = InscriptionForm
    success_url = reverse_lazy('connexion')

    def form_valid(self, form):
        #sauvegarde du user
        utilisateur= form.save(commit=False)
        utilisateur.first_name = form.cleaned_data['prenom']
        utilisateur.last_name = form.cleaned_data['nom']
        utilisateur.set_password(form.cleaned_data['mot_de_passe'])
        utilisateur.save()

        #succes
        messages.success(self.request, 'Inscription réussie ! Vous pouvez maintenant vous connecter.')
        return super().form_valid(form)

    def form_invalid(self, form):
        #erreur
        messages.error(self.request, "Veuillez corriger les erreurs du formulaire.")
        return super().form_invalid(form)

# def inscription(request):
#     if request.method == 'POST':
#         form = InscriptionForm(request.POST)
#         if form.is_valid():
#             utilisateur = form.save(commit=False)
#             utilisateur.first_name = form.cleaned_data['prenom']
#             utilisateur.last_name = form.cleaned_data['nom']
#             utilisateur.set_password(form.cleaned_data['mot_de_passe'])
#             utilisateur.save()
#             messages.success(request, "Inscription réussie ! Vous pouvez maintenant vous connecter.")
#             return redirect('inscription')  
#     else:
#         form = InscriptionForm()

#     return render(request, 'user/inscription.html', {'form': form})

class Connexion(LoginView):
    success_url = reverse_lazy('Accueil')
    template_name = 'user/connexion.html'
    redirect_authenticated_user = True

class Deconnexion(LogoutView):
    next_page = reverse_lazy('connexion')


class Accueil(LoginRequiredMixin,TemplateView):
    template_name= 'user/accueil.html'

    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context