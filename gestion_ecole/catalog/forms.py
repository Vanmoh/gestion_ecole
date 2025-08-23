# catalog/forms.py
from django import forms
from django.contrib.auth import get_user_model

from .models import SchoolYear, Grade, Classroom, Subject, Cycle, School

User = get_user_model()


# ---------------------------
# Années scolaires
# ---------------------------
class SchoolYearForm(forms.ModelForm):
    class Meta:
        model = SchoolYear
        fields = ["school", "label", "start_date", "end_date", "is_active"]
        widgets = {
            "start_date": forms.DateInput(attrs={"type": "date"}),
            "end_date": forms.DateInput(attrs={"type": "date"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["school"].empty_label = "— Sélectionner —"


# ---------------------------
# Niveaux (Grade)
# ---------------------------
class GradeForm(forms.ModelForm):
    class Meta:
        model = Grade
        fields = ["school", "name", "level"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["school"].empty_label = "— Sélectionner —"


# ---------------------------
# Classe (3 champs : École, Cycle, Nom)
# ---------------------------
class ClassroomAdvancedForm(forms.ModelForm):
    class Meta:
        model = Classroom
        # Le modèle Classroom doit avoir: school (FK), cycle (FK), label (CharField)
        fields = ["school", "cycle", "label"]
        widgets = {
            "label": forms.TextInput(attrs={
                "placeholder": "Nom de la classe",
                "list": "class-name-suggestions",  # utilisé par <datalist> dans le template
                "autocomplete": "off",
            })
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["school"].empty_label = "— Sélectionner —"
        self.fields["cycle"].empty_label = "— Sélectionner —"
        # Optionnel : ordonner les cycles par nom
        self.fields["cycle"].queryset = Cycle.objects.all().order_by("name")

    def clean_label(self):
        # Toujours stocker un libellé propre
        return (self.cleaned_data.get("label") or "").strip()


# Alias de compatibilité : si ailleurs on importe "ClassroomForm",
# on obtient bien ce nouveau formulaire 3 champs.
ClassroomForm = ClassroomAdvancedForm


# ---------------------------
# Matières
# ---------------------------
class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ["school", "name", "coefficient"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["school"].empty_label = "— Sélectionner —"


# ---------------------------
# Cycles
# ---------------------------
class CycleForm(forms.ModelForm):
    class Meta:
        model = Cycle
        fields = ["name", "notation"]
