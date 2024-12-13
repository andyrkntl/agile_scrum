from django.db import models

class Compte(models.Model):
    email_compte = models.EmailField(max_length=55, unique=True)
    mdp_compte = models.CharField(max_length=32)

    def __str__(self):
        return self.email_compte


class Personne(models.Model):
    ROLE_CHOICES = [
        ('organisateur', 'Organisateur'),
        ('participant', 'Participant'),
    ]
    id_compte = models.OneToOneField(Compte, on_delete=models.CASCADE)
    nom_prs = models.CharField(max_length=255)
    prenom_prs = models.CharField(max_length=126)
    email_prs = models.EmailField(max_length=32, unique=True)
    role_pers = models.CharField(max_length=32, choices=ROLE_CHOICES)

    def __str__(self):
        return f"{self.nom_prs} {self.prenom_prs} ({self.role_pers})"


class Evenement(models.Model):
    id_prs = models.ForeignKey(Personne, on_delete=models.CASCADE, related_name="evenements_crees")
    date_debut_event = models.DateTimeField()
    date_fin_event = models.DateTimeField()
    titre_event = models.CharField(max_length=32)
    lieu_event = models.CharField(max_length=32)
    description_event = models.CharField(max_length=255)
    disponibilite_event = models.CharField(max_length=128)

    def __str__(self):
        return self.titre_event


class Discuter(models.Model):
    id_prs = models.ForeignKey(Personne, on_delete=models.CASCADE, related_name="messages_envoyes")
    id_event = models.ForeignKey(Evenement, on_delete=models.CASCADE, related_name="messages")
    contenu_msg = models.TextField()
    date_envoi_msg = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message by {self.id_prs} in {self.id_event}"


class Participer(models.Model):
    id_event = models.ForeignKey(Evenement, on_delete=models.CASCADE, related_name="participants")
    id_prs = models.ForeignKey(Personne, on_delete=models.CASCADE, related_name="participations")
    ticket_virtuel = models.CharField(max_length=32)

    def __str__(self):
        return f"{self.id_prs} participates in {self.id_event}"


class Notifier(models.Model):
    id_event = models.ForeignKey(Evenement, on_delete=models.CASCADE, related_name="notifications")
    id_prs = models.ForeignKey(Personne, on_delete=models.CASCADE, related_name="notifications_recues")
    contenu_notif = models.CharField(max_length=255)
    date_notif = models.DateTimeField(auto_now_add=True)
    type_notif = models.CharField(max_length=128)

    def __str__(self):
        return f"Notification to {self.id_prs} about {self.id_event}"
