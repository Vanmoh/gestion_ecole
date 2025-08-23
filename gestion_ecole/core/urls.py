# core/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path("dashboard/", views.dashboard, name="dashboard"),
    path("switch/schoolyear/<int:pk>/", views.switch_schoolyear, name="switch_schoolyear"),
    path("switch/classroom/<int:pk>/", views.switch_classroom, name="switch_classroom"),  # optionnel
]
