from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.schemas import get_schema_view
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse, resolve

from project.views import (
    signup,
    ProjectViewset,
    CustomUserViewset,
    ContributorViewset,
    IssueViewset,
    CommentViewset,
)

from rest_framework_nested import routers

# Main router for ParentModel
main_router = routers.DefaultRouter()
main_router.register(r"projects", ProjectViewset, basename="project")
main_router.register(r"customuser", CustomUserViewset, basename="customuser")

# Nested router for ChildModels within Project
project_router = routers.NestedDefaultRouter(main_router, r"projects", lookup="project")
project_router.register(
    r"contributors", ContributorViewset, basename="project-contributor"
)
project_router.register(r"issues", IssueViewset, basename="project-issue")


issue_router = routers.NestedDefaultRouter(project_router, r"issues", lookup="issue")
issue_router.register(r"comments", CommentViewset, basename="comment")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api-auth/", include("rest_framework.urls")),
    path("", LoginView.as_view(), name="login", kwargs={"next_page": "/api/"}),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("signup/", signup, name="signup"),
    path("api/", include(main_router.urls)),
    path("api/", include(project_router.urls)),
    path("api/", include(issue_router.urls)),
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path(
        "openapi/",
        get_schema_view(
            title="SoftDesk API", description="API for all things", version="1.0.0"
        ),
        name="openapi-schema",
    ),
]


def get_url_names():
    url_names = []
    url_patterns = urlpatterns  # Get the root URL patterns

    def extract_url_names(patterns):
        for pattern in patterns:
            if hasattr(pattern, "url_patterns"):  # If it's a namespace, descend into it
                extract_url_names(pattern.url_patterns)
            elif hasattr(pattern, "name") and pattern.name is not None:
                url_names.append(pattern)

    extract_url_names(url_patterns)
    return url_names


all_url_names = get_url_names()
for name in all_url_names:
    print(name.name)
