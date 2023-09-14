from rest_framework.serializers import (
    HyperlinkedModelSerializer,
    SerializerMethodField,
    ModelSerializer,
)
from rest_framework.fields import CharField
from project.models import Comment, Contributor, CustomUser, Issue, Project
from rest_framework_nested.serializers import (
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


class CustomUserSignupSerializer(CustomUserSerializer):
    """Return a custom user serializer with every field plus an additional confirm password field"""

    password = CharField(style={"input_type": "password"})
    password_confirmation = CharField(style={"input_type": "password"})

    class Meta:
        model = CustomUser
        fields = (
            "username",
            "password",
            "password_confirmation",
            "can_be_contacted",
            "can_data_be_shared",
            "age",
        )


class ContributorSerializer(HyperlinkedModelSerializer):
    """Return a contributor serializer with every field."""

    class Meta:
        model = Contributor
        fields = ("url", "user", "project")


class IssueSerializer(HyperlinkedModelSerializer):
    """Return an issue serializer with every field."""

    comments = NestedHyperlinkedRelatedField(
        many=True,
        read_only=True,  # Or add a queryset
        view_name="project-issues-detail-comments-list",
        parent_lookup_kwargs={
            "project_pk": "project__uuid",
            "issue_pk": "uuid",
        },
    )

    comments_list_url = SerializerMethodField("get_comments_list_url", read_only=True)

    def get_comments_list_url(self, obj):
        request = self.context.get("request")
        if request is not None:
            return (
                f"{request.build_absolute_uri('/')[:-1]}{reverse_lazy('comment-list')}"
            )

    class Meta:
        model = Issue
        fields = (
            "url",
            "project",
            "assignee",
            "author",
            "status",
            "tag",
            "priority",
            "comments",
            "comments_list_url",
        )

    def create(self, validated_data):
        customuser = CustomUser.objects.get(
            username=self.context["request"].user.username
        )
        validated_data["author"] = customuser
        return super().create(validated_data)


class CommentSerializer(HyperlinkedModelSerializer):
    """Return a comment serializer with every field."""

    class Meta:
        model = Comment
        fields = "__all__"

    def create(self, validated_data):
        customuser = CustomUser.objects.get(
            username=self.context["request"].user.username
        )
        validated_data["author"] = customuser
        return super().create(validated_data)


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
            "project_type",
        )

    def create(self, validated_data):
        """Create a project with the current user as the author and add him to contributors"""
        print(self.context["request"].user.username)
        customuser = CustomUser.objects.get(
            username=self.context["request"].user.username
        )

        validated_data["author"] = customuser
        project = super().create(validated_data)
        contributor = Contributor.objects.create(user=customuser, project=project)
        contributor.save()
        return project
