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
                TokenObtainSerializer(data=form.data)
                return redirect("/api/")
            else:
                # We create the user if it does not exist
                user = CustomUser.objects.create_user(
                    username=form.data["username"],
                    password=form.data["password"],
                )
                authenticate(
                    username=form.data["username"],
                    password=form.data["password"],
                )
                TokenObtainSerializer(data=form.data)
                user.save()
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


class ProjectViewset(ModelViewSet):
    serializer_class = ProjectSerializer
    queryset = Project.objects.all()

    def get_permissions(self):
        """Instantiates and returns the list of permissions that this view requires."""
        return shared_get_permissions(self)


class ContributorViewset(ModelViewSet):
    serializer_class = ContributorSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get_queryset(self):
        if self.kwargs.get("project_pk"):
            return Contributor.objects.filter(project=self.kwargs["project_pk"])
        # list of contributors case
        return Contributor.objects.all()


class IssueViewset(ModelViewSet):
    serializer_class = IssueSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get_queryset(self):
        if self.kwargs.get("project_pk"):
            return Issue.objects.filter(project=self.kwargs["project_pk"])
        # list of issues case
        return Issue.objects.all()


class CommentViewset(ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get_queryset(self):
        if self.kwargs.get("issue_pk"):
            return Comment.objects.filter(issue=self.kwargs["issue_pk"])
        # list of comments case
        return Comment.objects.all()
