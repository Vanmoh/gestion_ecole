# students/models.py
from django.db import models
from django.utils.translation import gettext_lazy as _
from catalog.models import Classroom


class Student(models.Model):
    class Gender(models.TextChoices):
        MALE = "M", _("Masculin")
        FEMALE = "F", _("Féminin")

    # ——— Informations obligatoires (en base: tolère NULL pour migrer sereinement)
    last_name = models.CharField("Nom", max_length=100)
    first_name = models.CharField("Prénom", max_length=100)
    # mappe sur l’ancienne colonne 'birthdate'
    birth_date = models.DateField("Date de naissance", db_column="birthdate", null=True, blank=True)
    # nouveaux champs (ajoutés en base)
    city = models.CharField("Ville", max_length=100, null=True, blank=True)
    district = models.CharField("Quartier", max_length=100, null=True, blank=True)
    # mappe sur l’ancienne colonne 'sex'
    gender = models.CharField("Genre", db_column="sex", max_length=1, choices=Gender.choices, null=True, blank=True)
    photo = models.ImageField("Photo", upload_to="students/", null=True, blank=True)

    # ——— Informations supplémentaires
    # (évite unique=True pour ne pas échouer si tu as des doublons historiques)
    matricule = models.CharField("Matricule", max_length=50, null=True, blank=True)
    classroom = models.ForeignKey(
        Classroom, verbose_name="Classe",
        on_delete=models.SET_NULL, null=True, blank=True
    )
    enrollment_date = models.DateField("Date d'inscription", null=True, blank=True)
    parent_name = models.CharField("Nom du parent", max_length=150, null=True, blank=True)
    parent_phone = models.CharField("N° Téléphone du parent", max_length=50, null=True, blank=True)
    notes = models.TextField("Observation", null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["last_name", "first_name"]

    def __str__(self) -> str:
        return f"{self.last_name} {self.first_name}"







