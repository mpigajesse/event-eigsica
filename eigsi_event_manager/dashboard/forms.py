from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Utilisateur
from .models import Evenement


class UtilisateurForm(UserCreationForm):
    numero_telephone = forms.CharField(max_length=15, required=False)
    profile_picture = forms.ImageField(required=False)

    # Ajout d'un champ pour le rôle
    role = forms.ChoiceField(choices=Utilisateur.ROLE_CHOICES, required=True)

    class Meta:
        model = Utilisateur
        fields = [
            'username', 'nom', 'prenom', 'adresse_email', 'password1', 'password2', 
            'numero_telephone', 'profile_picture', 'role'
        ]



class EvenementForm(forms.ModelForm):
    class Meta:
        model = Evenement
        # Ajout des champs du modèle que l'on souhaite inclure dans le formulaire
        fields = ['titre','date_event', 'lieu', 'type', 'categorie_parascolaire', 'categorie_academique', 'acces_public', 'description', 'cover_img']
    
    def __init__(self, *args, **kwargs):
        super(EvenementForm, self).__init__(*args, **kwargs)
        # Définir le widget pour le champ 'type' avec les choix définis dans le modèle
        self.fields['type'].widget = forms.Select(choices=Evenement.TYPE_CHOICES)

        # Adapter les catégories en fonction du type d'événement sélectionné
        self.fields['categorie_parascolaire'].widget = forms.Select(choices=Evenement.CATEGORIE_PARASCOLAIRE_CHOICES)
        self.fields['categorie_academique'].widget = forms.Select(choices=Evenement.CATEGORIE_ACADEMIQUE_CHOICES)

        # Masquer les champs de catégorie qui ne devraient pas être affichés par défaut
        self.fields['categorie_parascolaire'].required = False  # Rendre ce champ facultatif
        self.fields['categorie_academique'].required = False    # Rendre ce champ facultatif

    def clean(self):
        cleaned_data = super().clean()
        evenement_type = cleaned_data.get('type')
        categorie_parascolaire = cleaned_data.get('categorie_parascolaire')
        categorie_academique = cleaned_data.get('categorie_academique')

        # Validation pour s'assurer qu'une catégorie appropriée est choisie en fonction du type
        if evenement_type == 'Parascolaire' and not categorie_parascolaire:
            self.add_error('categorie_parascolaire', "Veuillez sélectionner une catégorie parascolaire.")
        elif evenement_type == 'Académique' and not categorie_academique:
            self.add_error('categorie_academique', "Veuillez sélectionner une catégorie académique.")
