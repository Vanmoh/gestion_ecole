from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse
from django.views.generic import RedirectView  # ⇦ redirection vers login


def healthz(_):
    return HttpResponse("ok")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("healthz/", healthz),
    path("", RedirectView.as_view(url="/login/", permanent=False)),  # ⇦ redirection racine (login)
    path("", include("accounts.urls")),
    path("", include("catalog.urls")),
    path("", include("students.urls")),
    path("", include("core.urls")),

]
