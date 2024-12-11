from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password, check_password
from django.contrib import messages
from .models import Compte, Personne

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
            return redirect('home')
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
