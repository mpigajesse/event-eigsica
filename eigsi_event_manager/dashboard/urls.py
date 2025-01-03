from django.urls import path
from .views import *

app_name = 'dashboard'

urlpatterns = [
    path('', index, name='index'),  # Page d'accueil
    path('webevent/', webevent, name='webevent'),  # Route pour la page d'accueil du site
    path('add-user/', add_user, name='add-user'),
    path('login/', login_view, name='login'),  # Ajout de l'URL de connexion
    path('dashboard/', dashboard_view, name='dashboard'),  # Ajout de l'URL du tableau de bord
    path('logout/', logout_view, name='logout'),  # Ajout de l'URL de déconnexion
    path('profile/', profile_view, name='profile'),
    path('user-list/', user_list_view, name='user-list'),  # Ajout de l'URL pour la liste des utilisateurs
    path('add-event/', add_event_view, name='add-event'),
    path('event-list/', event_list_view, name='event-list'),
    path('event/update/<int:event_id>/', update_event, name='update-event'),
    path('event/delete/<int:event_id>/', delete_event, name='delete-event'),
    path('event/archive/<int:event_id>/', archive_event, name='archive-event'),  # Conservez cette ligne
    path('event/archive/', archive_list, name='archive-list'),  # URL pour la liste des archives
    path('event/publish/<int:event_id>/', publish_event, name='publish-event'),
    path('event/<int:event_id>/', detail_event, name='detail-event'),


   
]
