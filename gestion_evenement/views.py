from django.shortcuts import render, redirect, get_object_or_404
from django.utils.timezone import now
from django.contrib.auth.hashers import make_password, check_password
from django.contrib import messages
from .forms import EvenementForm
from .models import Compte, Personne, Evenement, Notifier, Participer
from django.contrib.auth.decorators import login_required

# Page d'accueil
def index(request):
    return render(request, "acceuil.html")

# Décorateurs personnalisés pour vérifier les rôles des utilisateurs
def organisateur_required(view_func):
    def wrapper(request, *args, **kwargs):
        utilisateur = get_object_or_404(Personne, id_compte=request.session.get('compte_id'))
        if utilisateur.role_pers != 'organisateur':
            messages.error(request, "Vous n'êtes pas autorisé à accéder à cette page.")
            return redirect(afficher_tous_evenements)
        return view_func(request, *args, **kwargs)
    return wrapper


# Inscription
def signup_view(request):
    if request.method == 'POST':
        email_compte = request.POST.get('email_compte')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')
        nom_prs = request.POST.get('nom_prs')
        prenom_prs = request.POST.get('prenom_prs')
        email_prs = request.POST.get('email_prs')
        role_pers = request.POST.get('role_pers')

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
        email_compte = request.POST.get('email_compte')
        password = request.POST.get('password')

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
    request.session.flush()
    messages.success(request, "Déconnexion réussie.")
    return redirect('login')

# Liste des événements accessibles
def afficher_tous_evenements(request):
    search_query = request.GET.get('search', '')
    start_date = request.GET.get('start_date', '')
    end_date = request.GET.get('end_date', '')

    evenements = Evenement.objects.filter(date_fin_event__gte=now()).order_by('date_debut_event')

    if search_query:
        evenements = evenements.filter(titre_event__icontains=search_query)

    if start_date:
        evenements = evenements.filter(date_debut_event__gte=start_date)

    if end_date:
        evenements = evenements.filter(date_fin_event__lte=end_date)

    utilisateur = get_object_or_404(Personne, id_compte=request.session.get('compte_id'))
    notifications = Notifier.objects.filter(id_prs=utilisateur).order_by('-date_notif')

    return render(request, 'evenement_principal.html', {
        'evenements': evenements,
        'notifications': notifications,
    })

# Création d'un événement (organisateur uniquement)
@organisateur_required
def creer_evenement(request):
    utilisateur = get_object_or_404(Personne, id_compte=request.session.get('compte_id'))

    if request.method == 'POST':
        form = EvenementForm(request.POST)
        if form.is_valid():
            evenement = form.save(commit=False)
            evenement.id_prs = utilisateur
            evenement.save()

            Notifier.objects.create(
                id_event=evenement,
                id_prs=utilisateur,
                contenu_notif=f"Vous avez créé l'événement '{evenement.titre_event}' pour le {evenement.date_debut_event}.",
                type_notif="Création"
            )

            messages.success(request, "Événement créé avec succès !")
            return redirect('afficher_org')
        else:
            messages.error(request, "Veuillez corriger les erreurs dans le formulaire.")
    else:
        form = EvenementForm()

    return render(request, 'creer_event.html', {'form': form})

# Liste des événements d'un organisateur

@organisateur_required
def afficher_org(request):
    utilisateur = get_object_or_404(Personne, id_compte=request.session.get('compte_id'))
    evenements = Evenement.objects.filter(id_prs=utilisateur)
    return render(request, 'evenement.html', {'evenements': evenements})

# Modification d'un événement (organisateur uniquement)
@organisateur_required
def modifier_evenement(request, evenement_id):
    utilisateur = get_object_or_404(Personne, id_compte=request.session.get('compte_id'))
    evenement = get_object_or_404(Evenement, id=evenement_id)

    if utilisateur != evenement.id_prs:
        messages.error(request, "Vous n'êtes pas autorisé à modifier cet événement.")
        return redirect('afficher_org')

    if request.method == 'POST':
        form = EvenementForm(request.POST, instance=evenement)
        if form.is_valid():
            evenement = form.save()
            Participer.objects.filter(id_event=evenement).update(
                id_prs=utilisateur
            )
            messages.success(request, "Événement modifié avec succès.")
            return redirect('afficher_org')
        else:
            messages.error(request, "Veuillez corriger les erreurs dans le formulaire.")
    else:
        form = EvenementForm(instance=evenement)

    return render(request, 'modifier_evenement.html', {'form': form})

# Suppression d'un événement (organisateur uniquement)
@organisateur_required
def supprimer_evenement(request, evenement_id):
    utilisateur = get_object_or_404(Personne, id_compte=request.session.get('compte_id'))
    evenement = get_object_or_404(Evenement, id=evenement_id)

    if utilisateur != evenement.id_prs:
        messages.error(request, "Vous n'êtes pas autorisé à supprimer cet événement.")
        return redirect('afficher_org')

    titre_event = evenement.titre_event
    evenement.delete()

    messages.success(request, f"L'événement '{titre_event}' a été supprimé.")
    return redirect('afficher_org')

def afficher_notifications(request):
    utilisateur = get_object_or_404(Personne, id_compte=request.session.get('compte_id'))
    notifications = Notifier.objects.filter(id_prs=utilisateur).order_by('-date_notif')
    return notifications

def afficher_detail_evenement(request, evenement_id):
    evenement = get_object_or_404(Evenement, id=evenement_id)
    return render(request, 'evenement_details.html', {'evenement': evenement})