from  .models import Notifier, Personne

def notifications_processor(request):
    if request.user.is_authenticated:
        utilisateur = Personne.objects.filter(id_compte=request.user.id).first()
        if utilisateur:
            notifications = Notifier.objects.filter(id_prs=utilisateur).order_by('-date_notif')[:10]
            return {'notifications': notifications}
    return {'notifications': []}
