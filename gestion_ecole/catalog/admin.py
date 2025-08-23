# catalog/admin.py
from django.contrib import admin
from .models import Classroom, Cycle, School, SchoolYear, Subject, Grade

@admin.register(Classroom)
class ClassroomAdmin(admin.ModelAdmin):
    list_display = ("label", "school", "cycle", "capacity", "main_teacher")
    list_filter = ("school", "cycle")
    # ✅ nécessaire pour que le widget d’autocomplete sur Classroom cherche quelque chose
    search_fields = ("label",)

# (facultatif) enregistrements simples pour le reste si pas déjà faits
@admin.register(Cycle)
class CycleAdmin(admin.ModelAdmin):
    list_display = ("name", "notation")
    search_fields = ("name",)

@admin.register(School)
class SchoolAdmin(admin.ModelAdmin):
    list_display = ("name", "address", "phone")
    search_fields = ("name", "address", "phone")

@admin.register(SchoolYear)
class SchoolYearAdmin(admin.ModelAdmin):
    list_display = ("school", "label", "start_date", "end_date", "is_active")
    list_filter = ("school", "is_active")
    search_fields = ("label",)

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ("school", "name", "coefficient")
    list_filter = ("school",)
    search_fields = ("name",)

@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ("school", "name", "level")
    list_filter = ("school",)
    search_fields = ("name",)
