"""budgetapi URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from allauth.account.views import ConfirmEmailView
from django.contrib import admin
from django.http import Http404
from django.shortcuts import redirect
from django.urls import include, path, re_path
from django.views.generic import RedirectView
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)


class CustomConfirmEmailView(ConfirmEmailView):
    """Confirm email on GET request."""

    def get(self, request, *args, **kwargs):
        try:
            self.object = self.get_object()
        except Http404:
            self.object = None
        # confirm email on get
        self.object.confirm(request)
        return redirect("rest_login")


urlpatterns = [
    path(
        "",
        RedirectView.as_view(url="/api/auth/login/?next=/api/v1/categories/"),
    ),
    path("admin/", admin.site.urls),
    path("api/v1/categories/", include("categories.urls")),
    path("api/v1/transactions/", include("transactions.urls")),
    path("api/auth/", include("rest_framework.urls")),
    path("api/v1/auth/", include("dj_rest_auth.urls")),
    re_path(
        "api/v1/auth/registration/account-confirm-email/(?P<key>.+)/",
        CustomConfirmEmailView.as_view(),
        name="account_confirm_email",
    ),
    path(
        "api/v1/auth/registration/", include("dj_rest_auth.registration.urls")
    ),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/schema/redoc/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc",
    ),
    path(
        "api/schema/swagger/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger",
    ),
]
