# students/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # Hub "Gestion des élèves" (accordéon avec 4 rubriques)
    path("students/", views.StudentsHubView.as_view(), name="students_home"),

    # 1. Liste des élèves
    path("students/list/", views.StudentListView.as_view(), name="student_list"),

    # 2. Inscription — Nouvel élève
    path("enroll/new/", views.StudentEnrollNewView.as_view(), name="student_enroll_new"),

    # 3. Inscription — Ancien élève
    path("enroll/old/", views.StudentEnrollOldView.as_view(), name="student_enroll_old"),

    #path("enroll/old/", views.StudentEnrollOldView.as_view(), name="enroll_old"),

    # 4. Tableau effectifs / statistiques
    path("enroll/stats/", views.StudentStatsView.as_view(), name="student_stats"),

    


    
]
