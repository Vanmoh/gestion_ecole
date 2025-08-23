# core/views.py
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from catalog.models import SchoolYear, Classroom
from students.models import Student

# Essaye d'importer Enrollment si le modèle existe encore.
try:
    from students.models import Enrollment  # type: ignore
except Exception:  # le modèle n'existe plus (nouvelle structure)
    Enrollment = None


@login_required
def dashboard(request):
    """
    Tableau de bord simple.
    - Si le modèle Enrollment existe : stats par année scolaire active.
    - Sinon : stats en direct sur Student (par classe).
    """
    sid = request.session.get("active_school_id")
    syid = request.session.get("active_schoolyear_id")

    context = {
        "active_school_id": sid,
        "active_schoolyear_id": syid,
        "per_class": [],
        "total_students": 0,
    }

    # Stats basées sur Enrollment (si dispo)
    if Enrollment is not None and syid:
        base = (
            Enrollment.objects
            .select_related("classroom")
            .filter(school_year_id=syid)
        )
        if sid:
            base = base.filter(classroom__school_id=sid)

        context["per_class"] = (
            base.values("classroom_id", "classroom__label")
                .annotate(total=Count("id"))
                .order_by("classroom__label")
        )
        context["total_students"] = base.count()
        return render(request, "dashboard.html", context)

    # Fallback sans Enrollment : regroupe les élèves par classe
    base_students = Student.objects.all()
    # Si on a un id d'école actif, on filtre via la classe (si renseignée)
    if sid:
        base_students = base_students.filter(classroom__school_id=sid)

    context["per_class"] = (
        base_students.values("classroom__id", "classroom__label")
        .annotate(total=Count("id"))
        .order_by("classroom__label")
    )
    context["total_students"] = base_students.count()
    return render(request, "dashboard.html", context)


@login_required
def switch_schoolyear(request, pk: int):
    """
    Active une année scolaire (stockée en session) et aligne l'école active dessus.
    """
    sy = get_object_or_404(SchoolYear, pk=pk)
    request.session["active_schoolyear_id"] = sy.id
    request.session["active_school_id"] = sy.school_id  # on cale l'école sur l'année
    messages.success(request, f"Année scolaire active : {sy.label}")
    # Retourne à la page précédente, sinon au dashboard
    return redirect(request.META.get("HTTP_REFERER") or reverse("dashboard"))


@login_required
def switch_classroom(request, pk: int):
    """
    Optionnel : mémorise une classe sélectionnée pour faciliter la navigation.
    """
    cls = get_object_or_404(Classroom, pk=pk)
    request.session["active_classroom_id"] = cls.id
    messages.info(request, f"Classe active : {cls.label}")
    return redirect(request.META.get("HTTP_REFERER") or reverse("dashboard"))
