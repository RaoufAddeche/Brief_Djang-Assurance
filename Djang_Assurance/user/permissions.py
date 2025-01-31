from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import redirect


class StaffRequiredMixin(UserPassesTestMixin):
    """
    Mixin pour vérifier que l'utilisateur est un membre du staff.

    Méthodes :
    ----------
    test_func():
        Vérifie si l'utilisateur connecté est un membre du staff.
    handle_no_permission():
        Redirige l'utilisateur vers la page de profil s'il n'a pas la permission.
    """

    def test_func(self):
        return self.request.user.is_staff

    def handle_no_permission(self):
        return redirect("profil")


class UserRequiredMixin(UserPassesTestMixin):
    """
    Mixin pour vérifier que l'utilisateur n'est pas un membre du staff.

    Méthodes :
    ----------
    test_func():
        Vérifie si l'utilisateur connecté n'est pas un membre du staff.
    handle_no_permission():
        Redirige l'utilisateur vers la page de profil s'il n'a pas la permission.
    """

    def test_func(self):
        return not self.request.user.is_staff

    def handle_no_permission(self):
        return redirect("profil")
