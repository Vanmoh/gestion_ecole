# catalog/views.py
from __future__ import annotations

import json
from django.utils.safestring import mark_safe

from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.decorators.http import require_GET
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from .models import SchoolYear, Grade, Classroom, Subject, Cycle, School
from .forms import (
    SchoolYearForm, GradeForm, SubjectForm, CycleForm,
    ClassroomAdvancedForm,  # <-- formulaire "École + Cycle (UI) + Nom"
)

# =========================================================
#                 Utilitaires multi-écoles
#   (Ici, les Cycles ne sont PAS filtrés par école, car
#    votre modèle Cycle courant n'a pas de champ `school`)
# =========================================================
def current_school(request):
    """Retourne l'école active (session), ou la 1re existante par défaut."""
    sid = request.session.get("school_id")
    school = School.objects.filter(id=sid).first() if sid else None
    if not school:
        school = School.objects.order_by("id").first()
        if school:
            request.session["school_id"] = school.id
    return school


@login_required
@require_GET
def switch_school(request, pk):
    """Change l'école active, puis revient à la page précédente."""
    school = get_object_or_404(School, pk=pk)
    request.session["school_id"] = school.id
    messages.info(request, f"École active : {school.name}")
    return redirect(request.META.get("HTTP_REFERER") or reverse("dashboard"))


# =========================
#        CATALOG (base)
# =========================

# ---------- SchoolYear ----------
class SchoolYearListView(LoginRequiredMixin, ListView):
    model = SchoolYear
    template_name = "catalog/school_year_list.html"
    context_object_name = "items"
    ordering = ["-is_active", "-start_date"]
    paginate_by = 50


class SchoolYearCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = "catalog.add_schoolyear"
    model = SchoolYear
    form_class = SchoolYearForm
    template_name = "catalog/form.html"
    success_url = reverse_lazy("school_year_list")

    def form_valid(self, form):
        messages.success(self.request, "Année scolaire créée.")
        return super().form_valid(form)


class SchoolYearUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = "catalog.change_schoolyear"
    model = SchoolYear
    form_class = SchoolYearForm
    template_name = "catalog/form.html"
    success_url = reverse_lazy("school_year_list")

    def form_valid(self, form):
        messages.success(self.request, "Année scolaire mise à jour.")
        return super().form_valid(form)


class SchoolYearDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    permission_required = "catalog.delete_schoolyear"
    model = SchoolYear
    template_name = "catalog/confirm_delete.html"
    success_url = reverse_lazy("school_year_list")

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Année scolaire supprimée.")
        return super().delete(request, *args, **kwargs)


# ---------- Grade ----------
class GradeListView(LoginRequiredMixin, ListView):
    model = Grade
    template_name = "catalog/grade_list.html"
    context_object_name = "items"
    ordering = ["level", "name"]


class GradeCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = "catalog.add_grade"
    model = Grade
    form_class = GradeForm
    template_name = "catalog/form.html"
    success_url = reverse_lazy("grade_list")

    def form_valid(self, form):
        messages.success(self.request, "Niveau créé.")
        return super().form_valid(form)


class GradeUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = "catalog.change_grade"
    model = Grade
    form_class = GradeForm
    template_name = "catalog/form.html"
    success_url = reverse_lazy("grade_list")

    def form_valid(self, form):
        messages.success(self.request, "Niveau mis à jour.")
        return super().form_valid(form)


class GradeDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    permission_required = "catalog.delete_grade"
    model = Grade
    template_name = "catalog/confirm_delete.html"
    success_url = reverse_lazy("grade_list")

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Niveau supprimé.")
        return super().delete(request, *args, **kwargs)


# ---------- Classroom (école + cycle + nom) ----------
# Presets pour les noms de classe selon le cycle
PRESETS_PRESCO = ["1ère Année", "2ème Année", "3ème Année"]
PRESETS_FOND1 = [
    "1ère Année", "2ème Année", "3ème Année", "4ème Année", "5ème Année",
    "6ème Année", "7ème Année", "8ème Année", "9ème Année",
]
PRESETS_FOND2 = ["7ème Année", "8ème Année", "9ème Année (DEF)"]
PRESETS_SECONDAIRE = [
    "10ème Année", "11ème Année", "12ème Année (Terminale)",
    "1ère Année", "2ème Année", "2ème Année (CAP)",
    "3ème Année (BT1)", "4ème Année (BT2)",
]
PRESETS_SUPERIEUR = [
    "Licence 1", "Licence 2", "Licence 3",
    "Master 1", "Master 2",
    "Doctorat 1", "Doctorat 2",
]

def presets_for_cycle_name(cycle_name: str) -> list[str]:
    """Retourne la liste de propositions de 'label' selon le nom du cycle."""
    if not cycle_name:
        return []
    n = cycle_name.lower()
    # Préscolaire (limité à 3ème Année)
    if any(k in n for k in ["présco", "presco", "jardin", "crèche", "creche"]):
        return PRESETS_PRESCO
    # Fondamental (1er cycle) complet (jusqu’à 9ème)
    if any(k in n for k in ["1er cycle", "premier cycle"]):
        return PRESETS_FOND1
    if any(k in n for k in ["2ème cycle", "2eme cycle", "deuxième cycle", "deuxieme cycle"]):
        return PRESETS_FOND2
    if any(k in n for k in ["secondaire", "lycée", "lycee", "technique", "professionnel"]):
        return PRESETS_SECONDAIRE
    if any(k in n for k in ["supérieure", "superieure", "universit"]):
        return PRESETS_SUPERIEUR
    return []


class ClassroomListView(LoginRequiredMixin, ListView):
    model = Classroom
    template_name = "settings/classroom_list.html"
    context_object_name = "items"
    paginate_by = 25
    ordering = ["label"]

    def get_queryset(self):
        # PAS de select_related('cycle') car Classroom n'a pas ce champ
        qs = Classroom.objects.select_related("school").order_by("label")
        q = self.request.GET.get("q", "").strip()
        if q:
            qs = qs.filter(
                Q(label__icontains=q) |
                Q(school__name__icontains=q)
            )
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["q"] = self.request.GET.get("q", "").strip()
        return ctx


class ClassroomCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = "catalog.add_classroom"
    model = Classroom
    form_class = ClassroomAdvancedForm
    template_name = "settings/classroom_form.html"
    success_url = reverse_lazy("classroom_list")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["request"] = self.request  # le form sait gérer 'request'
        return kwargs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        # Tous les cycles (pas de filtre par école)
        cycles = list(Cycle.objects.order_by("name").values("id", "name"))
        ctx["cycles_json"] = mark_safe(json.dumps(cycles))

        # presets initiaux (si l’utilisateur a déjà choisi un cycle en POST)
        cycle_name = ""
        if self.request.method == "POST":
            cid = self.request.POST.get("cycle")
            if cid and cid.isdigit():
                c = Cycle.objects.filter(pk=int(cid)).first()
                cycle_name = c.name if c else ""
        ctx["label_presets"] = presets_for_cycle_name(cycle_name)

        # Exposer aussi les constantes (utile pour un <datalist> côté template)
        ctx["PRESETS_PRESCO"] = PRESETS_PRESCO
        ctx["PRESETS_FOND1"] = PRESETS_FOND1
        ctx["PRESETS_FOND2"] = PRESETS_FOND2
        ctx["PRESETS_SECONDAIRE"] = PRESETS_SECONDAIRE
        ctx["PRESETS_SUPERIEUR"] = PRESETS_SUPERIEUR

        return ctx

    def form_valid(self, form):
        messages.success(self.request, "Classe créée.")
        return super().form_valid(form)


class ClassroomUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = "catalog.change_classroom"
    model = Classroom
    form_class = ClassroomAdvancedForm
    template_name = "settings/classroom_form.html"
    success_url = reverse_lazy("classroom_list")

    def get_queryset(self):
        return Classroom.objects.select_related("school")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["request"] = self.request
        return kwargs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        cycles = list(Cycle.objects.order_by("name").values("id", "name"))
        ctx["cycles_json"] = mark_safe(json.dumps(cycles))

        cycle_name = ""
        # si tu stockes un jour la relation cycle -> classroom, tu pourras remplir ici
        ctx["label_presets"] = presets_for_cycle_name(cycle_name)

        ctx["PRESETS_PRESCO_FOND1"] = PRESETS_PRESCO_FOND1
        ctx["PRESETS_FOND2"] = PRESETS_FOND2
        ctx["PRESETS_SECONDAIRE"] = PRESETS_SECONDAIRE
        ctx["PRESETS_SUPERIEUR"] = PRESETS_SUPERIEUR
        return ctx

    def form_valid(self, form):
        messages.success(self.request, "Classe mise à jour.")
        return super().form_valid(form)


class ClassroomDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    permission_required = "catalog.delete_classroom"
    model = Classroom
    template_name = "catalog/confirm_delete.html"
    success_url = reverse_lazy("classroom_list")

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Classe supprimée.")
        return super().delete(request, *args, **kwargs)


# ---------- Subject ----------
class SubjectListView(LoginRequiredMixin, ListView):
    model = Subject
    template_name = "catalog/subject_list.html"
    context_object_name = "items"
    ordering = ["name"]


class SubjectCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = "catalog.add_subject"
    model = Subject
    form_class = SubjectForm
    template_name = "catalog/form.html"
    success_url = reverse_lazy("subject_list")

    def form_valid(self, form):
        messages.success(self.request, "Matière créée.")
        return super().form_valid(form)


class SubjectUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = "catalog.change_subject"
    model = Subject
    form_class = SubjectForm
    template_name = "catalog/form.html"
    success_url = reverse_lazy("subject_list")

    def form_valid(self, form):
        messages.success(self.request, "Matière mise à jour.")
        return super().form_valid(form)


class SubjectDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    permission_required = "catalog.delete_subject"
    model = Subject
    template_name = "catalog/confirm_delete.html"
    success_url = reverse_lazy("subject_list")

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Matière supprimée.")
        return super().delete(request, *args, **kwargs)


# =========================
#          CYCLES
# =========================

# Suggestions pour le champ "Nom du cycle"
CYCLE_PRESETS = [
    "Préscolaire (Jardin d'enfant, Crèche)",
    "Fondamental (1er Cycle)",
    "Fondamental (2ème Cycle)",
    "Secondaire (Lycée, Technique, Professionnel)",
    "Supérieure (Universitaire)",
]
# Suggestions pour la notation
NOTATION_PRESETS = [10, 20, 100]


class CycleListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = "catalog.view_cycle"
    model = Cycle
    template_name = "settings/cycle_list.html"
    context_object_name = "items"
    paginate_by = 25

    def get_queryset(self):
        qs = Cycle.objects.all()  # pas de filtre par école
        q = self.request.GET.get("q", "").strip()
        if q:
            cond = Q(name__icontains=q)
            if q.isdigit():
                cond |= Q(notation=int(q))
            qs = qs.filter(cond)
        return qs.order_by("name")

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["q"] = self.request.GET.get("q", "").strip()
        return ctx


class CycleCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = "catalog.add_cycle"
    model = Cycle
    form_class = CycleForm
    template_name = "settings/cycle_form.html"
    success_url = reverse_lazy("cycle_list")

    def get_initial(self):
        initial = super().get_initial()
        initial.setdefault("notation", 20)
        return initial

    def form_valid(self, form):
        messages.success(self.request, "Cycle créé.")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["cycle_presets"] = CYCLE_PRESETS
        ctx["notation_presets"] = NOTATION_PRESETS
        return ctx


class CycleUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = "catalog.change_cycle"
    model = Cycle
    form_class = CycleForm
    template_name = "settings/cycle_form.html"
    success_url = reverse_lazy("cycle_list")

    def get_queryset(self):
        return Cycle.objects.all()  # pas de filtre par école

    def form_valid(self, form):
        messages.success(self.request, "Cycle modifié.")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["cycle_presets"] = CYCLE_PRESETS
        ctx["notation_presets"] = NOTATION_PRESETS
        return ctx


@login_required
@permission_required("catalog.delete_cycle")
def cycle_delete(request, pk):
    cycle = get_object_or_404(Cycle, pk=pk)  # pas de filtre par école
    if request.method == "POST":
        name = cycle.name
        cycle.delete()
        messages.success(request, f"Cycle « {name} » supprimé.")
    else:
        messages.error(request, "Suppression invalide.")
    q = request.POST.get("q") or request.GET.get("q", "")
    url = reverse("cycle_list")
    return redirect(f"{url}?q={q}" if q else url)












# ... imports et autres vues au-dessus ...

from django.utils.safestring import mark_safe
import json
from .forms import ClassroomAdvancedForm  # <= important

# --- presets (version « présco limité à 3e ») ---
PRESETS_PRESCO = ["1ère Année", "2ème Année", "3ème Année"]
PRESETS_FOND1 = [
    "1ère Année","2ème Année","3ème Année","4ème Année","5ème Année",
    "6ème Année","7ème Année","8ème Année","9ème Année",
]
PRESETS_FOND2 = ["7ème Année","8ème Année","9ème Année (DEF)"]
PRESETS_SECONDAIRE = [
    "10ème Année","11ème Année","12ème Année (Terminale)",
    "1ère Année","2ème Année","2ème Année (CAP)",
    "3ème Année (BT1)","4ème Année (BT2)",
]
PRESETS_SUPERIEUR = ["Licence 1","Licence 2","Licence 3","Master 1","Master 2","Doctorat 1","Doctorat 2"]

def presets_for_cycle_name(cycle_name: str):
    n = (cycle_name or "").lower()
    if any(k in n for k in ["présco","presco","jardin","crèche","creche"]):
        return PRESETS_PRESCO
    if any(k in n for k in ["1er cycle","premier cycle"]):
        return PRESETS_FOND1
    if any(k in n for k in ["2ème cycle","2eme cycle","deuxième cycle","deuxieme cycle"]):
        return PRESETS_FOND2
    if any(k in n for k in ["secondaire","lycée","lycee","technique","professionnel"]):
        return PRESETS_SECONDAIRE
    if any(k in n for k in ["supérieure","superieure","universit"]):
        return PRESETS_SUPERIEUR
    return []

class ClassroomListView(LoginRequiredMixin, ListView):
    model = Classroom
    template_name = "settings/classroom_list.html"
    context_object_name = "items"
    ordering = ["label"]
    paginate_by = 25
    def get_queryset(self):
        qs = Classroom.objects.select_related("school","cycle").order_by("label")
        q = self.request.GET.get("q","").strip()
        if q:
            qs = qs.filter(Q(label__icontains=q)|Q(cycle__name__icontains=q)|Q(school__name__icontains=q))
        return qs
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["q"] = self.request.GET.get("q","").strip()
        return ctx

class ClassroomCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = "catalog.add_classroom"
    model = Classroom
    form_class = ClassroomAdvancedForm
    template_name = "settings/classroom_form.html"
    success_url = reverse_lazy("classroom_list")
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["cycles_json"] = mark_safe(json.dumps(list(Cycle.objects.order_by("name").values("id","name"))))
        cid = self.request.POST.get("cycle")
        cycle_name = Cycle.objects.filter(pk=cid).values_list("name", flat=True).first() if cid else ""
        ctx["label_presets"] = presets_for_cycle_name(cycle_name)
        ctx["PRESETS_PRESCO"] = PRESETS_PRESCO
        ctx["PRESETS_FOND1"] = PRESETS_FOND1
        ctx["PRESETS_FOND2"] = PRESETS_FOND2
        ctx["PRESETS_SECONDAIRE"] = PRESETS_SECONDAIRE
        ctx["PRESETS_SUPERIEUR"] = PRESETS_SUPERIEUR
        return ctx
    def form_valid(self, form):
        messages.success(self.request, "Classe créée.")
        return super().form_valid(form)

class ClassroomUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = "catalog.change_classroom"
    model = Classroom
    form_class = ClassroomAdvancedForm
    template_name = "settings/classroom_form.html"
    success_url = reverse_lazy("classroom_list")
    def get_queryset(self):
        return Classroom.objects.select_related("school","cycle")
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["cycles_json"] = mark_safe(json.dumps(list(Cycle.objects.order_by("name").values("id","name"))))
        cycle_name = self.object.cycle.name if self.object and self.object.cycle_id else ""
        ctx["label_presets"] = presets_for_cycle_name(cycle_name)
        ctx["PRESETS_PRESCO"] = PRESETS_PRESCO
        ctx["PRESETS_FOND1"] = PRESETS_FOND1
        ctx["PRESETS_FOND2"] = PRESETS_FOND2
        ctx["PRESETS_SECONDAIRE"] = PRESETS_SECONDAIRE
        ctx["PRESETS_SUPERIEUR"] = PRESETS_SUPERIEUR
        return ctx
    def form_valid(self, form):
        messages.success(self.request, "Classe mise à jour.")
        return super().form_valid(form)
