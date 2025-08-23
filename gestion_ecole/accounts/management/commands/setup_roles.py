from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

# Modèles dont on configure les droits maintenant
from catalog.models import SchoolYear, Grade, Classroom, Subject
from students.models import Student, Enrollment

ROLE_DIRECTION   = "DIRECTION"
ROLE_ENSEIGNANT  = "ENSEIGNANT"
ROLE_COMPTABLE   = "COMPTABLE"

class Command(BaseCommand):
    help = "Crée les groupes de rôles et assigne les permissions de base"

    def handle(self, *args, **kwargs):
        # Crée les groupes s'ils n'existent pas
        g_dir, _ = Group.objects.get_or_create(name=ROLE_DIRECTION)
        g_prof, _ = Group.objects.get_or_create(name=ROLE_ENSEIGNANT)
        g_comp, _ = Group.objects.get_or_create(name=ROLE_COMPTABLE)

        def perms_for(model, actions=("add","change","delete","view")):
            ct = ContentType.objects.get_for_model(model)
            codes = [f"{a}_{model._meta.model_name}" for a in actions]
            return list(Permission.objects.filter(content_type=ct, codename__in=codes))

        # Direction : CRUD sur paramétrage + élèves/inscriptions (MVP)
        for model in (SchoolYear, Grade, Classroom, Subject, Student, Enrollment):
            g_dir.permissions.add(*perms_for(model, ("add","change","delete","view")))

        # Enseignant : lecture sur paramétrage + élèves/inscriptions (MVP)
        for model in (SchoolYear, Grade, Classroom, Subject, Student, Enrollment):
            g_prof.permissions.add(*perms_for(model, ("view",)))

        # Comptable : pour l’instant lecture des élèves (fees arriveront Sprint 6)
        for model in (Student, Enrollment):
            g_comp.permissions.add(*perms_for(model, ("view",)))

        self.stdout.write(self.style.SUCCESS("Groupes/permissions OK"))
