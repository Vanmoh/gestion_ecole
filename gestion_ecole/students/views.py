# students/views.py
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db.models import Q, Count
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, CreateView

from .models import Student
from .forms import StudentEnrollForm


# ——————————————————————————————————————
#  Page "Gestion des élèves" (hub / menu)
# ——————————————————————————————————————
class StudentsHubView(LoginRequiredMixin, TemplateView):
    """
    Affiche la page hub avec les 4 rubriques :
    - Liste des élèves
    - Inscription Nouvel Élève
    - Inscription Ancien Élève
    - Tableau effectifs
    """
    template_name = "students/index.html"


# ——————————————————————————————————————
#  Liste des élèves — pagination infinie
# ——————————————————————————————————————
class StudentListView(LoginRequiredMixin, ListView):
    model = Student
    template_name = "students/list.html"          # template "plein"
    context_object_name = "items"
    paginate_by = 50
    ordering = ["last_name", "first_name"]

    # permet de changer le pas via ?per=25|50|75|100…
    def get_paginate_by(self, queryset):
        try:
            return int(self.request.GET.get("per", self.paginate_by))
        except (TypeError, ValueError):
            return self.paginate_by

    # si ?partial=1 => on renvoie seulement les <tr> (fragment)
    def get_template_names(self):
        if self.request.GET.get("partial") == "1":
            return ["students/_student_rows.html"]
        return [self.template_name]

    def get_queryset(self):
        qs = (
            super()
            .get_queryset()
            .select_related("classroom", "classroom__cycle")
            .order_by(*self.ordering)
        )
        q = (self.request.GET.get("q") or "").strip()
        if q:
            qs = qs.filter(
                Q(last_name__icontains=q)
                | Q(first_name__icontains=q)
                | Q(matricule__icontains=q)
                | Q(classroom__label__icontains=q)
                | Q(classroom__cycle__name__icontains=q)
            )
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["q"] = (self.request.GET.get("q") or "").strip()
        try:
            ctx["per"] = int(self.request.GET.get("per", self.paginate_by))
        except (TypeError, ValueError):
            ctx["per"] = self.paginate_by
        return ctx


# ——————————————————————————————————————
#  Inscription — Nouvel élève
# ——————————————————————————————————————
class StudentEnrollNewView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = "students.add_student"
    model = Student
    form_class = StudentEnrollForm
    template_name = "students/enroll_new.html"
    success_url = reverse_lazy("student_list")

    def form_valid(self, form):
        messages.success(self.request, "Élève inscrit(e) avec succès.")
        return super().form_valid(form)


# ——————————————————————————————————————
#  Inscription — Ancien élève
# ——————————————————————————————————————
class StudentEnrollOldView(LoginRequiredMixin, TemplateView):
    """
    Page pour réinscrire un élève existant (contenu/logiciel libre).
    Tu peux y mettre un formulaire de recherche + mise à jour de classe/date.
    """
    template_name = "students/enroll_old.html"


# ——————————————————————————————————————
#  Tableau des effectifs / Statistiques
# ——————————————————————————————————————
class StudentStatsView(LoginRequiredMixin, TemplateView):
    template_name = "students/stats.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        # Effectifs par classe (None = sans classe)
        per_class = (
            Student.objects
            .values("classroom__id", "classroom__label")
            .annotate(total=Count("id"))
            .order_by("classroom__label")
        )
        ctx["per_class"] = per_class
        ctx["total_students"] = Student.objects.count()
        return ctx
