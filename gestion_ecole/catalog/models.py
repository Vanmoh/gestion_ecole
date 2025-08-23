# catalog/models.py
from django.db import models
from django.conf import settings


class School(models.Model):
    name = models.CharField(max_length=150)
    address = models.CharField(max_length=255, blank=True)
    phone = models.CharField(max_length=50, blank=True)

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name


class SchoolYear(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name="school_years")
    label = models.CharField(max_length=20)  # ex: 2025-2026
    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ("school", "label")
        ordering = ["-is_active", "-start_date"]

    def __str__(self) -> str:
        return f"{self.school} - {self.label}"


class Grade(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name="grades")
    name = models.CharField(max_length=50)   # ex: 6e, 3e, Tle
    level = models.IntegerField(default=0)

    class Meta:
        ordering = ["level", "name"]
        unique_together = ("school", "name")

    def __str__(self) -> str:
        return self.name


# ====== Cycle (unique définition) ======
class Cycle(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    notation = models.PositiveIntegerField(default=20)

    class Meta:
        ordering = ["name"]
        verbose_name = "Cycle"
        verbose_name_plural = "Cycles"

    def __str__(self) -> str:
        return self.name


class Classroom(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name="classrooms")

    # Nouveau lien : cycle choisi pour la classe
    cycle = models.ForeignKey(
        Cycle,
        on_delete=models.PROTECT,           # empêche la suppression d’un cycle utilisé
        null=True,
        blank=True,
        related_name="classrooms",
        verbose_name="Cycle",
    )

    label = models.CharField(max_length=50)  # ex: "3e A" ou "Licence 1"
    capacity = models.PositiveIntegerField(default=50)
    main_teacher = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="main_classes",
        verbose_name="Professeur principal",
    )

    class Meta:
        unique_together = ("school", "label")
        ordering = ["label"]
        verbose_name = "Classe"
        verbose_name_plural = "Classes"

    def __str__(self) -> str:
        return self.label


class Subject(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name="subjects")
    name = models.CharField(max_length=100)
    coefficient = models.DecimalField(max_digits=4, decimal_places=2, default=1)

    class Meta:
        unique_together = ("school", "name")
        ordering = ["name"]
        verbose_name = "Matière"
        verbose_name_plural = "Matières"

    def __str__(self) -> str:
        return self.name
