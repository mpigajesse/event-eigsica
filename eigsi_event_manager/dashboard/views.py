from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import UtilisateurForm, EvenementForm  # Assurez-vous que ce formulaire existe dans vos fichiers.
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Utilisateur, Evenement, ArchiveEvenement
from django.core.paginator import Paginator
from django.db.models import Q
from datetime import date
from django.utils import timezone

def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard:dashboard')

    if request.method == 'POST':
        username = request.POST.get('username') or request.POST.get('nom')
        password = request.POST.get('password') or request.POST.get('password1')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, "Connexion réussie !")
            return redirect('dashboard:dashboard')
        else:
            messages.error(request, "Nom d'utilisateur ou mot de passe invalide.")

    return render(request, 'dashboard/login.html')


def logout_view(request):
    logout(request)
    return redirect('dashboard:login')


@login_required
def dashboard_view(request):
    total_utilisateurs = Utilisateur.objects.count()
    total_evenements = Evenement.objects.count()
    total_evenements_non_publies = Evenement.objects.filter(status_publication='Non publié').count()
    total_evenements_publies = Evenement.objects.filter(status_publication='Publié').count()

    context = {
        'total_utilisateurs': total_utilisateurs,
        'total_evenements': total_evenements,
        'total_evenements_non_publies': total_evenements_non_publies,
        'total_evenements_publies': total_evenements_publies,
    }
    
    return render(request, 'dashboard/dashboard.html', context)


@login_required
def add_user(request):
    if request.method == 'POST':
        form = UtilisateurForm(request.POST, request.FILES)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            if Utilisateur.objects.filter(username=username).exists():
                messages.error(request, "Un utilisateur avec ce nom d'utilisateur existe déjà.")
            else:
                form.save()
                messages.success(request, "Utilisateur ajouté avec succès.")
                return redirect('dashboard:user-list')
    else:
        form = UtilisateurForm()
    
    return render(request, 'dashboard/add-user.html', {'form': form})


@login_required
def profile_view(request):
    user = request.user
    if request.method == 'POST':
        user.email = request.POST.get('email')
        user.username = request.POST.get('username')
        user.role = request.POST.get('role')
        user.affiliation = request.POST.get('affiliation')
        user.provenance = request.POST.get('provenance')
        user.phone = request.POST.get('phone')
        user.address = request.POST.get('address')

        if 'profile_picture' in request.FILES:
            user.profile_picture = request.FILES['profile_picture']

        user.save()
        messages.success(request, "Profil mis à jour avec succès.")
        return redirect('dashboard:profile')

    return render(request, 'dashboard/profile.html', {'user': user})


@login_required
def user_list_view(request):
    search_query = request.GET.get('search', '')
    if search_query:
        users = Utilisateur.objects.filter(
            Q(username__icontains=search_query) | 
            Q(nom__icontains=search_query) | 
            Q(prenom__icontains=search_query) | 
            Q(adresse_email__icontains=search_query) | 
            Q(numero_telephone__icontains=search_query) | 
            Q(role__icontains=search_query) |
            Q(email__icontains=search_query)
        )
    else:
        users = Utilisateur.objects.all()

    paginator = Paginator(users, 5)
    page_number = request.GET.get('page')
    users = paginator.get_page(page_number)

    return render(request, 'dashboard/user-list.html', {'users': users, 'search_query': search_query})


@login_required
def event_list_view(request):
    titre = request.GET.get('titre', '')
    search_query = request.GET.get('search', '')
    type_event = request.GET.get('type_event', '')
    categorie = request.GET.get('categorie', '')
    date_event = request.GET.get('date_event', '')
    lieu = request.GET.get('lieu', '')

    filters = Q()
    
    if titre:
        filters |= Q(titre__icontains=titre) | Q(description__icontains=titre)
    
    if search_query:
        filters |= Q(titre__icontains=search_query) | Q(description__icontains=search_query) | Q(lieu__icontains=search_query)
    
    if type_event:
        filters &= Q(type=type_event)
    
    if categorie:
        filters &= Q(categorie_parascolaire=categorie) | Q(categorie_academique=categorie)
    
    if date_event:
        filters &= Q(date_event__date=date_event)
    
    if lieu:
        filters &= Q(lieu__icontains=lieu)

    events = Evenement.objects.filter(filters, archived=False).order_by('-date_event')

    paginator = Paginator(events, 6)
    page_number = request.GET.get('page')
    events = paginator.get_page(page_number)

    categories_parascolaires = Evenement.CATEGORIE_PARASCOLAIRE_CHOICES
    categories_academiques = Evenement.CATEGORIE_ACADEMIQUE_CHOICES
    types_events = Evenement.TYPE_CHOICES

    return render(request, 'dashboard/event-list.html', {
        'events': events,
        'titre': titre,
        'search_query': search_query,
        'type_event': type_event,
        'categorie': categorie,
        'date_event': date_event,
        'lieu': lieu,
        'categories_parascolaires': categories_parascolaires,
        'categories_academiques': categories_academiques,
        'types_events': types_events,
    })


@login_required
def add_event_view(request):
    if request.method == 'POST':
        form = EvenementForm(request.POST, request.FILES)
        if form.is_valid():
            date_event = form.cleaned_data.get('date_event')
            if date_event and date_event.date() < timezone.now().date():
                messages.error(request, "La date de l'événement doit être aujourd'hui ou dans le futur.")
            else:
                form.save()
                messages.success(request, "L'événement a été ajouté avec succès.")
                return redirect('dashboard:event-list')
        else:
            messages.error(request, "Veuillez corriger les erreurs ci-dessous.")
    else:
        form = EvenementForm()

    return render(request, 'dashboard/add-event.html', {'form': form})


@login_required
def update_event(request, event_id):
    event = get_object_or_404(Evenement, id=event_id)

    if request.method == 'POST':
        date_event = request.POST.get('date_event')
        if date_event and date.fromisoformat(date_event) < timezone.now().date():
            messages.error(request, "La date de l'événement doit être aujourd'hui ou dans le futur.")
        else:
            event.titre = request.POST['titre']
            event.date_event = date_event
            event.lieu = request.POST['lieu']
            event.type = request.POST['type']
            event.categorie_parascolaire = request.POST.get('categorie_parascolaire')
            event.categorie_academique = request.POST.get('categorie_academique')
            event.acces_public = 'acces_public' in request.POST
            event.description = request.POST['description']

            if request.FILES.get('cover_img'):
                event.cover_img = request.FILES['cover_img']

            event.save()
            messages.success(request, "L'événement a été mis à jour avec succès.")
            return redirect('dashboard:event-list')

    return render(request, 'dashboard/update-event.html', {'event': event})


@login_required
def delete_event(request, event_id):
    event = get_object_or_404(Evenement, id=event_id)

    if request.method == "POST":
        event.delete()  # Supprime l'événement directement sans l'archiver
        messages.success(request, "L'événement a été supprimé avec succès.")
        return redirect('dashboard:event-list')

    return render(request, 'dashboard/event-list.html', {'event': event})


from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

@login_required
def archive_list(request):
    archived_events = ArchiveEvenement.objects.all()
    paginator = Paginator(archived_events, 8)  # Affiche 9 événements par page
    page_number = request.GET.get('page')
    
    try:
        archived_events = paginator.get_page(page_number)
    except PageNotAnInteger:
        archived_events = paginator.page(1)  # Retourne à la première page si `page` n'est pas un nombre
    except EmptyPage:
        archived_events = paginator.page(paginator.num_pages)  # Retourne à la dernière page si `page` est trop élevé

    if not archived_events:
        messages.info(request, "Aucun événement archivé à afficher.")

    return render(request, 'dashboard/archive-list.html', {'archives': archived_events})



@login_required
def archive_event(request, event_id):
    event = get_object_or_404(Evenement, id=event_id)
    
    if request.method == "POST":
        archive_evenement = ArchiveEvenement(
            evenement=event,
            utilisateur=request.user,
            titre=event.titre,
            description=event.description,
            lieu=event.lieu,
            date_event=event.date_event,
            type_event=event.type,
            categorie_parascolaire=event.categorie_parascolaire,
            categorie_academique=event.categorie_academique,
            acces_public=event.acces_public,
            cover_img=event.cover_img,
        )
        archive_evenement.save()
        event.archived = True
        event.save()
        messages.success(request, "L'événement a été archivé avec succès.")
        return redirect('dashboard:archive-list')

    return redirect('dashboard:event-list')


@login_required
def index(request):
    return render(request, 'website/index.html')
@login_required
def webevent(request):
    search_query = request.GET.get('search', '')
    type_event = request.GET.get('type_event', '')
    categorie = request.GET.get('categorie', '')
    date_event = request.GET.get('date_event', '')
    sort_option = request.GET.get('sort', 'date_desc')

    published_events = Evenement.objects.filter(status_publication="Publié")

    if search_query:
        published_events = published_events.filter(titre__icontains=search_query)

    if type_event:
        published_events = published_events.filter(type=type_event)

    if categorie:
        published_events = published_events.filter(categorie_parascolaire=categorie)

    if date_event:
        published_events = published_events.filter(date_event__date=date_event)

    if sort_option == 'date_asc':
        published_events = published_events.order_by('date_event')
    else:
        published_events = published_events.order_by('-date_event')

    paginator = Paginator(published_events, 6)
    page_number = request.GET.get('page')
    events_page = paginator.get_page(page_number)

    return render(request, 'website/webevent.html', {
        'events': events_page,
        'search_query': search_query,
        'type_event': type_event,
        'categorie': categorie,
        'date_event': date_event,
        'sort_option': sort_option,
        'types_events': Evenement.TYPE_CHOICES,
        'categories_parascolaires': Evenement.CATEGORIE_PARASCOLAIRE_CHOICES,
    })


@login_required
def publish_event(request, event_id):
    # Récupérer l'événement avec une vérification d'existence
    event = get_object_or_404(Evenement, id=event_id)
    
    # Vérification du rôle de l'utilisateur
    if request.user.role == 'Administrateur':
        event.publish_event()  # Supposant que cette méthode publie l'événement
        messages.success(request, "L'événement a été publié avec succès.")
        return redirect('dashboard:webevent')
    else:
        messages.error(request, "Vous n'avez pas l'autorisation de publier des événements.")
        return redirect('dashboard:event_list')  # Assurez-vous que 'event_list' est le bon nom de l'URL



def detail_event(request, event_id):
    event = get_object_or_404(Evenement, id=event_id)
    # Récupérer d'autres événements (exclure l'événement actuel)
    other_events = Evenement.objects.exclude(id=event_id).order_by('-date_event')[:10]  # Limitez à 5 événements
    
    context = {
        'event': event,
        'other_events': other_events,
    }
    return render(request, 'website/detail-event.html', context)
