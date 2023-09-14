from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.schemas import get_schema_view
from django.contrib.auth.views import LoginView, LogoutView

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
main_router.register(r"contributors", ContributorViewset, basename="contributor")
main_router.register(r"issues", IssueViewset, basename="issue")
main_router.register(r"comments", CommentViewset, basename="comment")

# Nested router for ChildModels within Project
project_router = routers.NestedDefaultRouter(main_router, r"projects", lookup="project")
project_router.register(
    r"contributors", ContributorViewset, basename="project-contributors"
)
project_router.register(r"issues", IssueViewset, basename="project-issues")


issue_router = routers.NestedDefaultRouter(project_router, r"issues", lookup="issue")
issue_router.register(r"comments", CommentViewset, basename="comment")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api-auth/", include("rest_framework.urls")),
    path("", LoginView.as_view(), name="login", kwargs={"next_page": "/api/"}),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("signup/", signup, name="signup"),
    path(r"api/", include(main_router.urls)),
    path(r"api/", include(project_router.urls)),
    path(r"api/", include(issue_router.urls)),
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
