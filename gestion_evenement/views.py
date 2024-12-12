from django.shortcuts import render, redirect, get_object_or_404
from django.utils.timezone import now
from django.contrib.auth.hashers import make_password, check_password
from .forms import EvenementForm
from django.contrib import messages
from .models import Compte, Personne , Evenement, Notifier, Participer
from django.contrib.auth.decorators import login_required


# Inscription
def signup_view(request):
    if request.method == 'POST':
        email_compte = request.POST['email_compte']
        password = request.POST['password']
        password_confirm = request.POST['password_confirm']
        nom_prs = request.POST['nom_prs']
        prenom_prs = request.POST['prenom_prs']
        email_prs = request.POST['email_prs']
        role_pers = request.POST['role_pers']

        if password != password_confirm:
            messages.error(request, "Les mots de passe ne correspondent pas.")
            return redirect('signup')

        if Compte.objects.filter(email_compte=email_compte).exists():
            messages.error(request, "Un compte avec cet email existe déjà.")
            return redirect('signup')

        compte = Compte.objects.create(
            email_compte=email_compte,
            mdp_compte=make_password(password)
        )

        Personne.objects.create(
            id_compte=compte,
            nom_prs=nom_prs,
            prenom_prs=prenom_prs,
            email_prs=email_prs,
            role_pers=role_pers
        )

        messages.success(request, "Inscription réussie. Vous pouvez vous connecter.")
        return redirect('login')

    return render(request, 'gestion_evenement/signup.html')

# Connexion
def login_view(request):
    if request.method == 'POST':
        email_compte = request.POST['email_compte']
        password = request.POST['password']

        try:
            compte = Compte.objects.get(email_compte=email_compte)
        except Compte.DoesNotExist:
            messages.error(request, "Email ou mot de passe incorrect.")
            return redirect('login')

        if check_password(password, compte.mdp_compte):
            request.session['compte_id'] = compte.id
            messages.success(request, "Connexion réussie.")
            return redirect('acceuil')
        else:
            messages.error(request, "Email ou mot de passe incorrect.")
            return redirect('login')

    return render(request, 'gestion_evenement/login.html')

# Déconnexion
def logout_view(request):
    if 'compte_id' in request.session:
        del request.session['compte_id']
        messages.success(request, "Déconnexion réussie.")
    return redirect('login')

# Page d'accueil (pour tester si connecté)
def home_view(request):
    compte_id = request.session.get('compte_id')
    if not compte_id:
        return redirect('login')

    compte = Compte.objects.get(id=compte_id)
    personne = Personne.objects.get(id_compte=compte)

    return render(request, 'gestion_evenement/home.html', {'personne': personne})

def index(request):
    return render (request,'acceuil.html')

# Fonction pour afficher la liste des événements avec filtres et recherche
def afficher_tous_evenements(request):
    search_query = request.GET.get('search', '')
    start_date = request.GET.get('start_date', '')
    end_date = request.GET.get('end_date', '')

    evenements = Evenement.objects.filter(date_fin_event__gte=now()).order_by('date_debut_event')

    # Appliquer la recherche par titre
    if search_query:
        evenements = evenements.filter(titre_event__icontains=search_query)
    
    # Appliquer les filtres par date
    if start_date:
        evenements = evenements.filter(date_debut_event__gte=start_date)
    if end_date:
        evenements = evenements.filter(date_debut_event__lte=end_date)
    
    return render(request, 'evenement_principal.html', {'evenements': evenements})

def creer_evenement(request):
    if request.method == 'POST':
        form = EvenementForm(request.POST)
        if form.is_valid():
            evenement = form.save(commit=False)
            organisateur = Personne.objects.get(id_compte=request.user.id)
            evenement.id_prs = organisateur
            evenement.save()

            Notifier.objects.create(
                id_event=evenement,
                id_prs=organisateur,
                contenu_notif=f"Vous avez créé l'événement '{evenement.titre_event}' pour le {evenement.date_debut_event}.",
                type_notif="Création"
            )
            return redirect('afficher_org')
    else:
        form = EvenementForm()

    return render(request, 'creer_event.html', {'form': form})

@login_required
def afficher_org(request):
    # Récupérer l'organisateur connecté
    organisateur = Personne.objects.get(id_compte=1)
    
    # Récupérer les événements de cet organisateur
    evenements = Evenement.objects.filter(id_prs=organisateur)
    
    return render(request, 'evenement.html', {'evenements': evenements})

# Fonction pour modifier un événement et notifier les participants
@login_required
def modifier_evenement(request, evenement_id):
    evenement = get_object_or_404(Evenement, id=evenement_id)

    if request.method == 'POST':
        evenement.titre_event = request.POST.get('titre_event')
        evenement.date_debut_event = request.POST.get('date_debut_event')
        evenement.date_fin_event = request.POST.get('date_fin_event')
        evenement.description_event = request.POST.get('description_event')
        evenement.save()

        # Notifier les participants
        participants = Participer.objects.filter(id_event=evenement)
        for participant in participants:
            Notifier.objects.create(
                id_event=evenement,
                id_prs=participant.id_prs,
                contenu_notif=f"L'événement '{evenement.titre_event}' a été modifié. Nouvelle date: {evenement.date_debut_event}.",
                type_notif="Modification"
            )
        return redirect('afficher_org')

    return render(request, 'modifier_evenement.html', {'evenement': evenement})

# Fonction pour supprimer un événement et notifier les participants

@login_required
def supprimer_evenement(request, evenement_id):
    evenement = get_object_or_404(Evenement, id=evenement_id)
    titre_event = evenement.titre_event
    participants = Participer.objects.filter(id_event=evenement)
    evenement.delete()

    # Notifier les participants
    for participant in participants:
        Notifier.objects.create(
            id_event=None,
            id_prs=participant.id_prs,
            contenu_notif=f"L'événement '{titre_event}' a été annulé.",
            type_notif="Suppression"
        )
    return redirect('afficher_org')

# Fonction pour afficher les notifications
@login_required
def afficher_toutes_notifications(request):
    utilisateur = get_object_or_404(Personne, id_compte=request.user.id)
    notifications = Notifier.objects.filter(id_prs=utilisateur).order_by('-date_notif')
    # return render(request, 'notifications.html', {'notifications': notifications})
    return redirect('index')

