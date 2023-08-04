from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from project.views import login_page, signup, logout_user

from project.views import (
    ProjectViewset,
    CustomUserViewset,
    ContributorViewset,
    IssueViewset,
    CommentViewset,
)

router = routers.SimpleRouter()
router.register("customuser", CustomUserViewset, basename="customuser")
router.register("contributor", ContributorViewset, basename="contributor")
router.register("issue", IssueViewset, basename="issue")
router.register("comment", CommentViewset, basename="comment")
router.register("project", ProjectViewset, basename="project")

urlpatterns = [
    path("", login_page, name="login"),
    path("logout/", logout_user, name="logout"),
    path("signup/", signup, name="signup"),
    path("admin/", admin.site.urls),
    path("api-auth/", include("rest_framework.urls")),
    path("api/", include(router.urls)),
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
