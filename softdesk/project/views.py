from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from project.models import Project, CustomUser, Contributor, Issue, Comment
from project.serializers import (
    ProjectSerializer,
    CustomUserSerializer,
    ContributorSerializer,
    CustomUserSignupSerializer,
    IssueSerializer,
    CommentSerializer,
)
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render


def login_page(request):
    form = CustomUserSerializer()
    message = ""
    if request.method == "POST":
        form = CustomUserSerializer(data=request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data["username"],
                password=form.cleaned_data["password"],
            )
            custom_user = CustomUser.objects.get(user=user)
            if user is not None:
                login(request, user)
                return redirect("project")
        message = "Identifiants invalides."
    return render(
        request, "authentication/login.html", context={"form": form, "message": message}
    )


def signup(request):
    form = CustomUserSignupSerializer()
    message = ""
    if request.method == "POST":
        form = CustomUserSignupSerializer(data=request.POST)
        if form.is_valid():
            # We authenticate the user to log him in if the account already exists
            user = authenticate(
                username=form.cleaned_data["username"],
                password=form.cleaned_data["password"],
            )
            if user is not None:
                login(request, user)
                return redirect("home")
            else:
                # We create the user if it does not exist
                user = CustomUser.objects.create_user(
                    username=form.cleaned_data["username"],
                    password=form.cleaned_data["password"],
                )
                user.save()
                login(request, user)
                return redirect("home")
    return render(
        request,
        "authentication/signup.html",
        context={"form": form, "message": message},
    )


def logout_user(request):
    logout(request)
    return redirect("login")


class ProjectViewset(ModelViewSet):
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get_queryset(self):
        return Project.objects.all()


class CustomUserViewset(ReadOnlyModelViewSet):
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get_queryset(self):
        return CustomUser.objects.all()


class ContributorViewset(ModelViewSet):
    serializer_class = ContributorSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get_queryset(self):
        return Contributor.objects.all()


class IssueViewset(ModelViewSet):
    serializer_class = IssueSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get_queryset(self):
        return Issue.objects.all()


class CommentViewset(ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get_queryset(self):
        return Comment.objects.all()
