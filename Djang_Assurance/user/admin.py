from django.contrib import admin
from .models import CustomUser, StaffUser

# Enregistrement des modèles dans l'interface d'administration
admin.site.register(CustomUser)  # Permet de gérer les utilisateurs personnalisés via l'admin
admin.site.register(StaffUser)  # Permet de gérer les membres du personnel via l'admin