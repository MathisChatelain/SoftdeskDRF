from rest_framework.serializers import ModelSerializer

from project.models import Comment, Contributor, CustomUser, Issue, Project


class CustomUserSerializer(ModelSerializer):
    """Return a custom user serializer with every field."""

    class Meta:
        model = CustomUser
        fields = "__all__"


class ProjectSerializer(ModelSerializer):
    """Return a project serializer with every field."""

    class Meta:
        model = Project
        fields = "__all__"


class ContributorSerializer(ModelSerializer):
    """Return a contributor serializer with every field."""

    class Meta:
        model = Contributor
        fields = "__all__"


class IssueSerializer(ModelSerializer):
    """Return an issue serializer with every field."""

    class Meta:
        model = Issue
        fields = "__all__"


class CommentSerializer(ModelSerializer):
    """Return a comment serializer with every field."""

    class Meta:
        model = Comment
        fields = "__all__"
