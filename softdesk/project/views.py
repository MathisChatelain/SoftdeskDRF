from rest_framework.viewsets import ModelViewSet
from project.models import Project, CustomUser, Contributor, Issue, Comment
from project.serializers import (
    ProjectSerializer,
    CustomUserSerializer,
    CustomUserSignupSerializer,
    ContributorSerializer,
    IssueSerializer,
    CommentSerializer,
)
from rest_framework_simplejwt.serializers import TokenObtainSerializer
from rest_framework.permissions import (
    IsAuthenticated,
    IsAdminUser,
)
from django.contrib.auth import authenticate
from django.shortcuts import redirect, render
from project.permissions import shared_get_permissions


def signup(request):
    form = CustomUserSignupSerializer()
    message = ""
    has_error = False
    if request.method == "POST":
        form = CustomUserSignupSerializer(data=request.POST)
        is_valid = form.is_valid()
        if is_valid:
            # We authenticate the user to log him in if the account already exists
            user = CustomUser.objects.filter(
                username=form.data["username"],
                password=form.data["password"],
            )
            if len(user) == 1:
                TokenObtainSerializer(data=form.data).validate(form.data)
                return redirect("/api/")
            else:
                # We create the user if it does not exist
                user = CustomUser.objects.create_user(
                    username=form.data["username"],
                    password=form.data["password"],
                )
                # Django Authentication
                authenticate(
                    username=form.data["username"],
                    password=form.data["password"],
                )
                # DRF-SimpleJWT Authentication
                TokenObtainSerializer(data=form.data).validate(form.data)
                return redirect("/api/")
        else:
            message = "Please correct the errors below"
            has_error = True
    return render(
        request,
        "registration/signup.html",
        context={"form": form, "message": message, "has_error": has_error},
    )


class CustomUserViewset(ModelViewSet):
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
    queryset = CustomUser.objects.all()


class PermissionMixin:
    def get_permissions(self):
        """Instantiates and returns the list of permissions that this view requires."""
        return shared_get_permissions(self)


class ProjectViewset(ModelViewSet, PermissionMixin):
    serializer_class = ProjectSerializer
    queryset = Project.objects.all()


class ContributorViewset(ModelViewSet, PermissionMixin):
    serializer_class = ContributorSerializer

    def get_queryset(self):
        if self.kwargs.get("project_pk"):
            return Contributor.objects.filter(project=self.kwargs["project_pk"])
        return Contributor.objects.all()  # list of contributors case


class IssueViewset(ModelViewSet, PermissionMixin):
    serializer_class = IssueSerializer

    def get_queryset(self):
        if self.kwargs.get("project_pk"):
            return Issue.objects.filter(project=self.kwargs["project_pk"])
        return Issue.objects.all()  # list of issues case


class CommentViewset(ModelViewSet, PermissionMixin):
    serializer_class = CommentSerializer

    def get_queryset(self):
        if self.kwargs.get("issue_pk"):
            return Comment.objects.filter(issue=self.kwargs["issue_pk"])
        return Comment.objects.all()  # list of comments case
