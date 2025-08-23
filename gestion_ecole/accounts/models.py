from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    class Role(models.TextChoices):
        ADMIN = "ADMIN", "Admin système"
        DIRECTION = "DIRECTION", "Direction"
        ENSEIGNANT = "ENSEIGNANT", "Enseignant"
        SURVEILLANT = "SURVEILLANT", "Surveillant"
        COMPTABLE = "COMPTABLE", "Comptable"
        PARENT = "PARENT", "Parent"
        ELEVE = "ELEVE", "Élève"

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.DIRECTION)
    phone = models.CharField(max_length=30, blank=True)

    def __str__(self):
        return f"{self.user.username} ({self.role})"
