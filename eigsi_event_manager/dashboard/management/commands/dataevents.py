import os
import requests
from django.core.files import File
from django.core.management.base import BaseCommand
from django.utils import timezone
from dashboard.models import Evenement  # Remplacez `your_app` par le nom de votre application
from io import BytesIO
from django.core.files.base import ContentFile
import random

class Command(BaseCommand):
    help = "Remplit la table 'Evenement' avec des données factices et télécharge des images thématiques depuis Unsplash"

    def handle(self, *args, **kwargs):
        # Types et catégories d'événements pour générer des événements variés
        type_choix = ['Parascolaire', 'Académique']
        categorie_parascolaire = ['Sportive', 'Culturel', 'Artistique']
        categorie_academique = ['Certifications', 'Concours', 'Conférences']
        lieu_choices = ['Casablanca', 'Marrakech', 'Rabat', 'Agadir']

        # Liste de mots-clés thématiques
        themes = [
            "événements", "école", "ingénierie", "IA", "Énergie", 
            "BIGDATA", "IT", "Base de données", "Business intelligent", 
            "EIGSICA", "EIGSI LA ROCHELLE", "Étudiant", "ingénieur", 
            "Marrakech", "Casablanca", "Maroc", "culture marocaine", 
            "français", "africain", "technologie", "innovation", 
            "startups", "intelligence artificielle", "machine learning", 
            "réseaux", "cybersécurité", "data science", "cloud computing", 
            "smart cities", "économie circulaire", "développement durable", 
            "projets étudiants", "hackathons", "conférences", "ateliers", 
            "éducation", "collaboration", "leadership", "entrepreneuriat", 
            "design thinking", "transformation numérique", "analytique", 
            "système d'information", "mobilité", "infrastructure", 
            "culture africaine", "art contemporain", "patrimoine", 
            "gastronomie marocaine", "musique", "traditions", 
            "diversité culturelle", "jeunesse", "engagement communautaire", 
            "bénévolat", "formation professionnelle", "certifications", 
            "compétences numériques"
        ]

        # Clé API Unsplash
        UNSPLASH_ACCESS_KEY = 'bu5iGYTuEOxPa6uW-Ng0g0wYp_c24REc1OIGPkxIhyU'  # Remplacez par votre clé API Unsplash

        for i in range(10):  # Génère 10 événements
            theme_titre = random.choice(themes)  # Choisit un thème pour le titre
            titre = theme_titre  # Utilise uniquement le thème pour le titre
            date_event = timezone.now() + timezone.timedelta(days=random.randint(1, 30))
            lieu = random.choice(lieu_choices)
            type_event = random.choice(type_choix)

            # Sélectionne la catégorie en fonction du type d'événement
            if type_event == 'Parascolaire':
                categorie_parascolaire_value = random.choice(categorie_parascolaire)
                categorie_academique_value = None
                query = categorie_parascolaire_value
            else:
                categorie_academique_value = random.choice(categorie_academique)
                categorie_parascolaire_value = None
                query = categorie_academique_value

            # Ajoute un mot-clé aléatoire à la requête
            theme_query = random.choice(themes)

            # Télécharge une image depuis Unsplash en utilisant le thème de l'événement
            response = requests.get(
                f"https://api.unsplash.com/photos/random",
                headers={"Authorization": f"Client-ID {UNSPLASH_ACCESS_KEY}"},
                params={"query": theme_query, "orientation": "landscape"}
            )
            
            if response.status_code == 200:
                img_data = response.json()
                img_url = img_data["urls"]["regular"]
                img_response = requests.get(img_url)
                
                if img_response.status_code == 200:
                    img_name = f"event_{i+1}.jpg"
                    image_content = ContentFile(img_response.content)

                    # Crée l'événement avec les données factices
                    evenement = Evenement(
                        titre=titre,
                        date_event=date_event,
                        lieu=lieu,
                        type=type_event,
                        categorie_parascolaire=categorie_parascolaire_value,
                        categorie_academique=categorie_academique_value,
                        acces_public=random.choice([True, False]),
                        # Description incluant le thème de l'événement
                        description=(
                            f"Cet événement, intitulé '{titre}', est axé sur le thème '{theme_query}'. "
                            f"Il abordera des sujets tels que {query}, et se déroulera à {lieu} le {date_event.strftime('%Y-%m-%d')}."
                        ),
                        status_publication=random.choice(['Publié', 'Non publié']),
                    )
                    
                    # Sauvegarde l'image téléchargée
                    evenement.cover_img.save(img_name, image_content, save=True)
                    self.stdout.write(self.style.SUCCESS(f"L'événement '{titre}' a été ajouté avec une image thématique."))

                else:
                    self.stdout.write(self.style.ERROR("Échec du téléchargement de l'image depuis Unsplash."))
            else:
                self.stdout.write(self.style.ERROR("Échec de la requête API Unsplash pour le thème d'image."))
