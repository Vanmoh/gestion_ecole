# catalog/urls.py
from django.urls import path
from . import views

from django.urls import path
from .views import (
    switch_school,
    SchoolYearListView, SchoolYearCreateView, SchoolYearUpdateView, SchoolYearDeleteView,
    GradeListView, GradeCreateView, GradeUpdateView, GradeDeleteView,
    ClassroomListView, ClassroomCreateView, ClassroomUpdateView, ClassroomDeleteView,
    SubjectListView, SubjectCreateView, SubjectUpdateView, SubjectDeleteView,
    CycleListView, CycleCreateView, CycleUpdateView, cycle_delete,
)


urlpatterns = [
    # Switch d’école
    path("switch-school/<int:pk>/", views.switch_school, name="switch_school"),

    # Années scolaires
    path("settings/school-years/", views.SchoolYearListView.as_view(), name="school_year_list"),
    path("settings/school-years/new", views.SchoolYearCreateView.as_view(), name="school_year_new"),
    path("settings/school-years/<int:pk>/edit", views.SchoolYearUpdateView.as_view(), name="school_year_edit"),
    path("settings/school-years/<int:pk>/delete", views.SchoolYearDeleteView.as_view(), name="school_year_delete"),

    # Niveaux (Grades)
    path("settings/grades/", views.GradeListView.as_view(), name="grade_list"),
    path("settings/grades/new", views.GradeCreateView.as_view(), name="grade_new"),
    path("settings/grades/<int:pk>/edit", views.GradeUpdateView.as_view(), name="grade_edit"),
    path("settings/grades/<int:pk>/delete", views.GradeDeleteView.as_view(), name="grade_delete"),

    # Classes
    path("settings/classes/", views.ClassroomListView.as_view(), name="classroom_list"),
    path("settings/classes/new", views.ClassroomCreateView.as_view(), name="classroom_new"),
    path("settings/classes/<int:pk>/edit", views.ClassroomUpdateView.as_view(), name="classroom_edit"),
    path("settings/classes/<int:pk>/delete", views.ClassroomDeleteView.as_view(), name="classroom_delete"),

    # Matières
    path("settings/subjects/", views.SubjectListView.as_view(), name="subject_list"),
    path("settings/subjects/new", views.SubjectCreateView.as_view(), name="subject_new"),
    path("settings/subjects/<int:pk>/edit", views.SubjectUpdateView.as_view(), name="subject_edit"),
    path("settings/subjects/<int:pk>/delete", views.SubjectDeleteView.as_view(), name="subject_delete"),

    # Cycles
    path("settings/cycles/", views.CycleListView.as_view(), name="cycle_list"),
    path("settings/cycles/new", views.CycleCreateView.as_view(), name="cycle_new"),
    path("settings/cycles/<int:pk>/edit", views.CycleUpdateView.as_view(), name="cycle_edit"),
    path("settings/cycles/<int:pk>/delete", views.cycle_delete, name="cycle_delete"),
]
