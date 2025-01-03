from django.contrib import admin
from .models import Utilisateur, Etudiant, Administrateur, Evenement, Invite

# Vérifiez si Utilisateur est déjà enregistré
if 'dashboard.Utilisateur' in admin.site._registry:
    admin.site.unregister(Utilisateur)

@admin.register(Utilisateur)
class UtilisateurAdmin(admin.ModelAdmin):
    list_display = ('username', 'nom', 'prenom', 'adresse_email', 'numero_telephone', 'role', 'profile_picture')
    list_filter = ('role',)
    search_fields = ('username', 'nom', 'prenom', 'adresse_email')

@admin.register(Etudiant)
class EtudiantAdmin(admin.ModelAdmin):
    list_display = ('utilisateur', 'promotion', 'dominante')
    search_fields = ('utilisateur__nom', 'utilisateur__prenom', 'promotion')

@admin.register(Administrateur)
class AdministrateurAdmin(admin.ModelAdmin):
    list_display = ('utilisateur', 'affiliation')
    search_fields = ('utilisateur__nom', 'utilisateur__prenom', 'affiliation')

@admin.register(Evenement)
class EvenementAdmin(admin.ModelAdmin):
    list_display = ('lieu', 'date_event', 'acces_public', 'type', 'categorie_parascolaire', 'categorie_academique')
    list_filter = ('acces_public', 'type', 'categorie_parascolaire', 'categorie_academique')
    search_fields = ('lieu', 'categorie_parascolaire', 'categorie_academique', 'description')

@admin.register(Invite)
class InviteAdmin(admin.ModelAdmin):
    list_display = ('evenement', 'provenance')
    search_fields = ('provenance', 'evenement__categorie__nom')  # Modification : Utilisation de 'evenement__categorie__nom' pour des recherches plus précises
