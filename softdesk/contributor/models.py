from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """
    Définit les utilisateurs, avec leur âge, leur choix de consentement
    Les données d'authentification sont gérées par Django
    """

    age = models.IntegerField(null=True)
    consent = models.BooleanField(default=False)


class Contributor(models.Model):
    """
    Définit les utilisateurs qui sont contributeurs d'un projet spécifique… Un utilisateur peut
    contribuer à plusieurs projets, et un projet peut avoir plusieurs contributeurs. Le
    contributeur peut créer trois types de ressources: le project, l'issue et le comment.
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey("Project", on_delete=models.CASCADE)

    class Meta:
        unique_together = ["user", "project"]
