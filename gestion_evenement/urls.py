from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name="acceuil"),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('créer_evenement/', views.creer_evenement, name='creer_evenement'),
    path('liste_des_evenements/', views.afficher_org, name='afficher_org'),
    path('evenement/modifier/<int:evenement_id>/', views.modifier_evenement, name='modifier_evenement'),
    path('evenement/supprimer/<int:evenement_id>/', views.supprimer_evenement, name='supprimer_evenement'),
    path('evenement/',views.afficher_tous_evenements,name='afficher_tous'),
    path('notification/',views.afficher_notifications,name="afficher_notifications"),
    path('evenement/<int:evenement_id>/', views.afficher_detail_evenement, name='detail_evenement'),
]
