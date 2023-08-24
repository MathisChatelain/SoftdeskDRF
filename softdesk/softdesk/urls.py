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
# main_router.register(r"contributor", ContributorViewset, basename="contributor")
# main_router.register(r"issue", IssueViewset, basename="issue")
# main_router.register(r"comment", CommentViewset, basename="comment")

# Nested router for ChildModel within ParentModel
project_router = routers.NestedSimpleRouter(main_router, r"projects", lookup="project")
project_router.register(r"contributors", ContributorViewset, basename="contributor")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api-auth/", include("rest_framework.urls")),
    path("", LoginView.as_view(), name="login", kwargs={"next_page": "/api/"}),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("signup/", signup, name="signup"),
    path("api/", include(main_router.urls)),
    path("api/", include(project_router.urls)),
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
