# students/admin.py
from django.contrib import admin
from .models import Student

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ("last_name", "first_name", "gender", "classroom", "matricule", "enrollment_date")
    list_filter = ("gender", "classroom")
    # ✅ requis quand on utilise autocomplete_fields quelque part
    search_fields = ("last_name", "first_name", "matricule", "parent_phone", "city", "district")
    # champ FK -> widget d’autocomplétion
    autocomplete_fields = ("classroom",)
