from django.db import models
from django.contrib.auth.models import User


class CustomUser(User):
    """
    Définit les utilisateurs, avec leur âge, leur choix de consentement
    Les données d'authentification sont gérées par Django
    """

    age = models.IntegerField(null=True)
    can_be_contacted = models.BooleanField(default=False)
    can_data_be_shared = models.BooleanField(default=False)


class Project(models.Model):
    """
    Définit les projets, avec leur nom, leur date de création et leur date de
    mise à jour. Un projet peut avoir plusieurs contributeurs.
    """

    name = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    contributors = models.ManyToManyField(CustomUser, through="Contributor")
    author = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="author"
    )
    description = models.TextField()


class Contributor(models.Model):
    """
    Définit les utilisateurs qui sont contributeurs d'un projet spécifique… Un utilisateur peut
    contribuer à plusieurs projets, et un projet peut avoir plusieurs contributeurs. Le
    contributeur peut créer trois types de ressources: le project, l'issue et le comment.
    """

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    class Meta:
        unique_together = ["user", "project"]


class Issue(models.Model):
    """
    Définit les problèmes d'un projet, ainsi que son statut, sa priorité, son attribution
    (utilisateur auquel le problème est affecté), sa balise (bug, tâche, amélioration).
    Un project peut posséder plusieurs issues, mais une issue n'est rattachée qu'à un seul project.
    """

    status = models.CharField(max_length=128)
    priority = models.CharField(max_length=128)
    assignee = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    tag = models.CharField(max_length=128)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    contributor = models.ForeignKey("Contributor", on_delete=models.CASCADE)


class Comment(models.Model):
    """
    Définit les commentaires d'un problème (issue) particulier. Une issue peut avoir
    plusieurs comments, mais un comment n'est rattaché qu'à une seule issue.
    """

    content = models.TextField()
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE)
    contributor = models.ForeignKey("Contributor", on_delete=models.CASCADE)
