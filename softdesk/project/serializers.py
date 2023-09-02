from rest_framework.serializers import (
    HyperlinkedModelSerializer,
    SerializerMethodField,
    ModelSerializer,
)
from rest_framework.fields import CharField
from project.models import Comment, Contributor, CustomUser, Issue, Project
from rest_framework_nested.serializers import (
    NestedHyperlinkedModelSerializer,
    NestedHyperlinkedRelatedField,
)
from django.urls import reverse_lazy


class CustomUserSerializer(ModelSerializer):
    """Return a custom user serializer with every field."""

    class Meta:
        model = CustomUser
        fields = (
            "uuid",
            "url",
            "username",
            "projects",
            "age",
            "can_be_contacted",
            "can_data_be_shared",
        )


class CustomUserUsernameSerializer(CustomUserSerializer):
    class Meta:
        model = CustomUser
        fields = ("username",)


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


class ContributorSerializer(HyperlinkedModelSerializer):
    """Return a contributor serializer with every field."""

    class Meta:
        model = Contributor
        fields = ("url", "user", "project")


class ContributorURLSerializer(ContributorSerializer):
    """Return a contributor serializer with only the url field."""

    class Meta:
        model = Contributor
        fields = ("url",)


class IssueSerializer(NestedHyperlinkedModelSerializer):
    """Return an issue serializer with every field."""

    class Meta:
        model = Issue
        fields = "__all__"


class IssueURLSerializer(IssueSerializer):
    """Return an issue serializer with only the url field."""

    class Meta:
        model = Issue
        fields = ("url",)


class CommentSerializer(NestedHyperlinkedModelSerializer):
    """Return a comment serializer with every field."""

    class Meta:
        model = Comment
        fields = "__all__"


class CommentURLSerializer(CommentSerializer):
    """Return a comment serializer with only the url field."""

    class Meta:
        model = Comment
        fields = ("url",)


class ProjectSerializer(HyperlinkedModelSerializer):
    """Return a project serializer with every field. and it's nested contributors and issues"""

    # method field to get the url of the contributors
    contributors_list_url = SerializerMethodField(
        "get_contributors_list_url", read_only=True
    )

    def get_contributors_list_url(self, obj):
        request = self.context.get("request")
        if request is not None:
            return f"{request.build_absolute_uri('/')[:-1]}{reverse_lazy('project-contributors-list', args=[obj.uuid])}"

    contributors = NestedHyperlinkedRelatedField(
        many=True,
        read_only=True,  # Or add a queryset
        view_name="project-contributors-detail",
        parent_lookup_kwargs={"project_pk": "project__uuid"},
    )

    issues_list_url = SerializerMethodField("get_issues_list_url", read_only=True)

    def get_issues_list_url(self, obj):
        request = self.context.get("request")
        if request is not None:
            return f"{request.build_absolute_uri('/')[:-1]}{reverse_lazy('project-issues-list', args=[obj.uuid])}"

    issues = NestedHyperlinkedRelatedField(
        many=True,
        read_only=True,  # Or add a queryset
        view_name="project-issues-detail",
        parent_lookup_kwargs={"project_pk": "project__uuid"},
    )

    class Meta:
        model = Project
        fields = (
            "uuid",
            "url",
            "name",
            "description",
            "contributors_list_url",
            "contributors",
            "issues_list_url",
            "issues",
            "author",
            "project_type",
        )
