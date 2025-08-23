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
#  Liste des élèves
# ——————————————————————————————————————
class StudentListView(LoginRequiredMixin, ListView):
    model = Student
    template_name = "students/list.html"
    context_object_name = "items"
    paginate_by = 50
    ordering = ["last_name", "first_name"]

    def get_queryset(self):
        qs = super().get_queryset()
        q = (self.request.GET.get("q") or "").strip()
        if q:
            qs = qs.filter(
                Q(last_name__icontains=q) |
                Q(first_name__icontains=q) |
                Q(matricule__icontains=q)
            )
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["q"] = (self.request.GET.get("q") or "").strip()
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













# students/views.py (ajout)
from django.views.generic.edit import FormView
from .forms import StudentEnrollOldForm
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin

class StudentEnrollOldView(LoginRequiredMixin, FormView):
    template_name = "students/enroll_old.html"
    form_class = StudentEnrollOldForm
    success_url = reverse_lazy("student_list")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["school_id"] = self.request.session.get("active_school_id")
        return kwargs

    def form_valid(self, form):
        student = form.cleaned_data["student"]
        classroom = form.cleaned_data["classroom"]
        enrollment_date = form.cleaned_data["enrollment_date"]
        notes = form.cleaned_data.get("notes", "")

        # Inscrire l’ancien élève : on met à jour sa classe + date + notes
        student.classroom = classroom
        student.enrollment_date = enrollment_date
        if notes:
            # Concaténer proprement si des notes existent déjà
            student.notes = (student.notes + "\n" if student.notes else "") + notes
        student.save()

        messages.success(
            self.request,
            f"Inscription (ancien élève) enregistrée pour {student.last_name} {student.first_name} en {classroom.label}."
        )
        return super().form_valid(form)
