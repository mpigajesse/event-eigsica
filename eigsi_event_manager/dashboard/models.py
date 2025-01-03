import os
from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save, pre_save, pre_delete
from django.dispatch import receiver
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.core.exceptions import ValidationError


class Utilisateur(AbstractUser):
    ROLE_CHOICES = [
        ('Administrateur', 'Administrateur'),
        ('Étudiant', 'Étudiant'),
        ('Invité', 'Invité'),
    ]
    
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    adresse_email = models.EmailField(unique=True)
    numero_telephone = models.CharField(max_length=15, null=True, blank=True)
    mot_de_passe = models.CharField(max_length=128, null=True)
    role = models.CharField(max_length=30, choices=ROLE_CHOICES, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)

    def __str__(self):
        return f"{self.nom} {self.prenom} - {self.role or 'Utilisateur'}"


class Etudiant(models.Model):
    utilisateur = models.OneToOneField(Utilisateur, on_delete=models.CASCADE)
    promotion = models.CharField(max_length=100)
    dominante = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.utilisateur.nom} {self.utilisateur.prenom}"


class Administrateur(models.Model):
    utilisateur = models.OneToOneField(Utilisateur, on_delete=models.CASCADE)
    affiliation = models.CharField(max_length=100)

    def __str__(self):
        return f"Administrateur: {self.utilisateur.nom} {self.utilisateur.prenom}"


class Evenement(models.Model):
    TYPE_CHOICES = [
        ('Parascolaire', 'Parascolaire'),
        ('Académique', 'Académique'),
    ]

    CATEGORIE_PARASCOLAIRE_CHOICES = [
        ('Sportive', 'Sportive'),
        ('Culturel', 'Culturel'),
        ('Artistique', 'Artistique'),
    ]

    CATEGORIE_ACADEMIQUE_CHOICES = [
        ('Certifications', 'Certifications'),
        ('Concours', 'Concours'),
        ('Conférences', 'Conférences'),
    ]

    STATUT_CHOICES = [
        ('Non publié', 'Non publié'),
        ('Publié', 'Publié'),
    ]

    status_publication = models.CharField(
        max_length=20,
        choices=STATUT_CHOICES,
        default='Non publié',  # Valeur par défaut corrigée pour assurer que tous les nouveaux événements soient "Non publié".
    )
    titre = models.CharField(max_length=100)
    date_event = models.DateTimeField()
    lieu = models.CharField(max_length=100)
    type = models.CharField(max_length=50, choices=TYPE_CHOICES)
    categorie_parascolaire = models.CharField(max_length=50, choices=CATEGORIE_PARASCOLAIRE_CHOICES, blank=True, null=True)
    categorie_academique = models.CharField(max_length=50, choices=CATEGORIE_ACADEMIQUE_CHOICES, blank=True, null=True)
    acces_public = models.BooleanField(default=True)
    description = models.TextField()
    cover_img = models.ImageField(upload_to='covers/', null=True, blank=True)
    archived = models.BooleanField(default=False)  # Indique si l'événement est archivé

    def __str__(self):
        if self.type == 'Parascolaire':
            return f"{self.categorie_parascolaire} à {self.lieu} le {self.date_event}"
        elif self.type == 'Académique':
            return f"{self.categorie_academique} à {self.lieu} le {self.date_event}"
        return f"Événement à {self.lieu} le {self.date_event}"

    def clean(self):
        if self.date_event < timezone.now():
            raise ValidationError("La date de l'événement doit être aujourd'hui ou dans le futur.")

    def save(self, *args, **kwargs):
        if not self.pk:  # Vérifie si l'événement est nouveau
            self.status_publication = 'Non publié'
        self.clean()
        super().save(*args, **kwargs)
        
    def publish_event(self):
        self.status_publication = 'Publié'
        self.save()


class Invite(models.Model):
    evenement = models.ForeignKey(Evenement, on_delete=models.CASCADE, related_name='invites')
    provenance = models.CharField(max_length=100)
    utilisateur = models.ForeignKey(Utilisateur, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"Invite de {self.provenance} pour l'événement {self.evenement}"


class ArchiveEvenement(models.Model):
    evenement = models.OneToOneField(Evenement, on_delete=models.CASCADE, related_name='archive')
    date_archivage = models.DateTimeField(auto_now_add=True)
    utilisateur = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)

    titre = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    lieu = models.CharField(max_length=100)
    date_event = models.DateTimeField()
    type_event = models.CharField(max_length=50, choices=Evenement.TYPE_CHOICES)
    categorie_parascolaire = models.CharField(max_length=50, choices=Evenement.CATEGORIE_PARASCOLAIRE_CHOICES, blank=True, null=True)
    categorie_academique = models.CharField(max_length=50, choices=Evenement.CATEGORIE_ACADEMIQUE_CHOICES, blank=True, null=True)
    acces_public = models.BooleanField(default=True)
    cover_img = models.ImageField(upload_to='archive_covers/', null=True, blank=True)

    def __str__(self):
        return f"Archive de l'événement: {self.titre} (Archivé le {self.date_archivage})"


@receiver(post_save, sender=Utilisateur)
def create_profile_directory(sender, instance, created, **kwargs):
    if created:
        profile_pictures_dir = os.path.join(settings.MEDIA_ROOT, 'profile_pictures')
        if not os.path.exists(profile_pictures_dir):
            os.makedirs(profile_pictures_dir)

        if instance.role == 'Administrateur':
            Administrateur.objects.create(utilisateur=instance)
        elif instance.role == 'Étudiant':
            Etudiant.objects.create(utilisateur=instance)


@receiver(pre_save, sender=Evenement)
def create_event_cover_directory(sender, instance, **kwargs):
    covers_dir = os.path.join(settings.MEDIA_ROOT, 'covers')
    if not os.path.exists(covers_dir):
        os.makedirs(covers_dir)


@receiver(pre_delete, sender=Evenement)
def archive_event_before_deletion(sender, instance, **kwargs):
    ArchiveEvenement.objects.create(
        evenement=instance,
        titre=instance.titre,
        description=instance.description,
        lieu=instance.lieu,
        date_event=instance.date_event,
        type_event=instance.type,
        categorie_parascolaire=instance.categorie_parascolaire,
        categorie_academique=instance.categorie_academique,
        acces_public=instance.acces_public,
        cover_img=instance.cover_img
    )


@receiver(post_save, sender=ArchiveEvenement)
def create_archive_cover_directory(sender, instance, created, **kwargs):
    if created:
        archive_covers_dir = os.path.join(settings.MEDIA_ROOT, 'archive_covers')
        if not os.path.exists(archive_covers_dir):
            os.makedirs(archive_covers_dir)





class Participant(models.Model):
    utilisateur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE, related_name="participations")
    evenement = models.ForeignKey(Evenement, on_delete=models.CASCADE, related_name="participants")
    date_inscription = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('utilisateur', 'evenement')
        verbose_name = "Participation"
        verbose_name_plural = "Participations"

    def clean(self):
        # Empêcher l'inscription si un autre événement auquel l'utilisateur participe chevauche cet événement
        conflicting_events = Participant.objects.filter(
            utilisateur=self.utilisateur,
            evenement__date_event__date=self.evenement.date_event.date(),
            evenement__date_event__time=self.evenement.date_event.time()
        ).exclude(evenement=self.evenement)

        if conflicting_events.exists():
            raise ValidationError("Vous êtes déjà inscrit à un autre événement à la même heure.")

    def save(self, *args, **kwargs):
        self.clean()  # Validation pour vérifier le conflit d'événements avant l'enregistrement
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.utilisateur} participe à {self.evenement}"
