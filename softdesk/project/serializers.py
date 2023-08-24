from rest_framework.serializers import HyperlinkedModelSerializer
from rest_framework.fields import CharField
from project.models import Comment, Contributor, CustomUser, Issue, Project
from rest_framework_nested.serializers import NestedHyperlinkedModelSerializer
from rest_framework_nested.relations import NestedHyperlinkedRelatedField


class CustomUserSerializer(HyperlinkedModelSerializer):
    """Return a custom user serializer with every field."""

    class Meta:
        model = CustomUser
        fields = (
            "uuid",
            "username",
            "age",
            "can_be_contacted",
            "can_data_beshared",
        )


class CustomUserSignupSerializer(CustomUserSerializer):
    """Return a custom user serializer with every field plus an additional confirm password field"""

    password_confirmation = CharField()

    class Meta:
        model = CustomUser
        fields = (
            "username",
            "password",
            "password_confirmation",
            "can_be_contacted",
            "can_data_be_shared",
        )


class ProjectSerializer(HyperlinkedModelSerializer):
    """Return a project serializer with every field."""

    class Meta:
        model = Project
        fields = "__all__"


class ContributorSerializer(NestedHyperlinkedModelSerializer):
    """Return a contributor serializer with every field."""

    parent_lookup_kwargs = {
        "project_pk": "project",
    }

    class Meta:
        model = Contributor
        fields = "__all__"


class IssueSerializer(HyperlinkedModelSerializer):
    """Return an issue serializer with every field."""

    class Meta:
        model = Issue
        fields = "__all__"


class CommentSerializer(HyperlinkedModelSerializer):
    """Return a comment serializer with every field."""

    class Meta:
        model = Comment
        fields = "__all__"
