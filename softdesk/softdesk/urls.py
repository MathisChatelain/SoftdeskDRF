from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.schemas import get_schema_view
from django.contrib.auth.views import LoginView, LogoutView

from project.views import (
    SignupView,
    ProjectViewset,
    CustomUserViewset,
    ContributorViewset,
    IssueViewset,
    CommentViewset,
)

router = routers.DefaultRouter()
router.register("customuser", CustomUserViewset, basename="customuser")
router.register("contributor", ContributorViewset, basename="contributor")
router.register("issue", IssueViewset, basename="issue")
router.register("comment", CommentViewset, basename="comment")
router.register("project", ProjectViewset, basename="project")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api-auth/", include("rest_framework.urls")),
    path("", LoginView.as_view(), name="login", kwargs={"next_page": "/api/"}),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("signup/", SignupView.as_view(), name="signup"),
    path("api/", include(router.urls)),
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
