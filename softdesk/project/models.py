from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from uuid import uuid4


class CustomUser(User):
    """
    Définit les utilisateurs, avec leur âge, leur choix de consentement
    Les données d'authentification sont gérées par Django
    """

    uuid = models.UUIDField(
        primary_key=True, editable=False, unique=True, default=uuid4()
    )
    age = models.IntegerField(null=True)
    can_be_contacted = models.BooleanField(default=False)
    can_data_be_shared = models.BooleanField(default=False)
    created_at = models.DateTimeField(editable=False, default=datetime.now())
    updated_at = models.DateTimeField(default=datetime.now())

    def save(self, *args, **kwargs):
        """On save, update timestamps"""
        if not self.uuid:
            self.created_at = datetime.now()
        self.updated_at = datetime.now()
        return super(CustomUser, self).save(*args, **kwargs)


class BaseModel(models.Model):
    """
    Classe abstraite qui définit les champs communs à tous les modèles.
    """

    uuid = models.UUIDField(
        primary_key=True, editable=False, unique=True, default=uuid4()
    )
    created_at = models.DateTimeField(editable=False, default=datetime.now())
    updated_at = models.DateTimeField(default=datetime.now())
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)

    def save(self, *args, **kwargs):
        """On save, update timestamps"""
        if not self.uuid:
            self.created_at = datetime.now()
        self.updated_at = datetime.now()
        return super(BaseModel, self).save(*args, **kwargs)

    class Meta:
        abstract = True
        ordering = ["-created_at"]


class Project(BaseModel):
    """
    Définit les projets, avec leur nom, leur date de création et leur date de
    mise à jour. Un projet peut avoir plusieurs contributeurs.
    """

    name = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    description = models.TextField()

    PROJECT_TYPE_CHOICES = [
        ("BACKEND", "Backend"),
        ("FRONTEND", "Frontend"),
        ("IOS", "iOS"),
        ("ANDROID", "Android"),
    ]
    project_type = models.CharField(
        max_length=128, choices=PROJECT_TYPE_CHOICES, default="BACKEND"
    )


class Contributor(BaseModel):
    """
    Définit les utilisateurs qui sont contributeurs d'un projet spécifique… Un utilisateur peut
    contribuer à plusieurs projets, et un projet peut avoir plusieurs contributeurs. Le
    contributeur peut créer trois types de ressources: le project, l'issue et le comment.
    """

    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="projects"
    )
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name="contributors"
    )

    class Meta:
        unique_together = ["user", "project"]


class Issue(BaseModel):
    """
    Définit les problèmes d'un projet, ainsi que son statut, sa priorité, son attribution
    (utilisateur auquel le problème est affecté), sa balise (bug, tâche, amélioration).
    Un project peut posséder plusieurs issues, mais une issue n'est rattachée qu'à un seul project.
    """

    assignee = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="assignee"
    )
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name="issues"
    )
    # - Nous pouvons donner une priorité à l’issue (LOW, MEDIUM ou HIGH) pour connaître son importance.
    PRIORITY_CHOICES = [
        ("LOW", "Low"),
        ("MEDIUM", "Medium"),
        ("HIGH", "High"),
    ]
    priority = models.CharField(max_length=128, choices=PRIORITY_CHOICES, default="LOW")
    # Nous pouvons aussi donner une balise (BUG, FEATURE ou TASK) pour connaître la nature de l’issue.
    TAG_CHOICES = [
        ("BUG", "Bug"),
        ("FEATURE", "Feature"),
        ("TASK", "Task"),
    ]
    tag = models.CharField(max_length=128, choices=TAG_CHOICES, default="FEATURE")

    # - Enfin, les contributeurs doivent pouvoir émettre un statut de progression
    # (ToDo, In Progress ou Finished). Par défaut, une issue est en To Do.
    STATUS_CHOICES = [
        ("TODO", "To Do"),
        ("INPROGRESS", "In Progress"),
        ("FINISHED", "Finished"),
    ]
    status = models.CharField(max_length=128, choices=STATUS_CHOICES, default="TODO")


class Comment(BaseModel):
    """
    Définit les commentaires d'un problème (issue) particulier. Une issue peut avoir
    plusieurs comments, mais un comment n'est rattaché qu'à une seule issue.
    """

    content = models.TextField()
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE)
    contributor = models.ForeignKey("Contributor", on_delete=models.CASCADE)
