from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('', views.home_view, name='home'),
    path('Acceuil',views.index,name="acceuil"),
    path('Créer_evenement/', views.creer_evenement, name='creer_evenement'),
    path('Liste_des_evenements/', views.afficher_org, name='afficher_org'),
    path('Evenement/modifier/<int:evenement_id>/', views.modifier_evenement, name='modifier_evenement'),
    path('Evenement/supprimer/<int:evenement_id>/', views.supprimer_evenement, name='supprimer_evenement'),
    path('Evenement/',views.afficher_tous_evenements,name='afficher_tous'),
    path('Notification/',views.afficher_notifications)
]
