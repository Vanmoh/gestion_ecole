# students/urls.py
from django.urls import path
from .views import (
    StudentsHubView,
    StudentListView,
    StudentEnrollNewView,
    StudentEnrollOldView,
    StudentStatsView,
)

# Optionnel : utile si tu veux namespacer plus tard (ex: 'students:student_list')
app_name = "students"

urlpatterns = [
    # Hub "Gestion des élèves"
    path("students/", StudentsHubView.as_view(), name="students_home"),

    # 1) Liste des élèves (scroll infini via ?page=N&partial=1)
    path("students/list/", StudentListView.as_view(), name="student_list"),

    # 2) Inscription — Nouvel élève
    path("students/enroll/new/", StudentEnrollNewView.as_view(), name="student_enroll_new"),
    # Alias compat (anciens liens)
    path("enroll/new/", StudentEnrollNewView.as_view(), name="student_enroll_new_legacy"),

    # 3) Inscription — Ancien élève
    path("students/enroll/old/", StudentEnrollOldView.as_view(), name="student_enroll_old"),
    # Alias compat (anciens liens)
    path("enroll/old/", StudentEnrollOldView.as_view(), name="student_enroll_old_legacy"),

    # 4) Tableau effectifs / statistiques
    path("students/stats/", StudentStatsView.as_view(), name="student_stats"),
]
