# students/forms.py
from django import forms
from .models import Student
from catalog.models import Classroom


class StudentEnrollForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = [
            # Obligatoires
            "last_name", "first_name", "birth_date", "city", "district", "gender", "photo",
            # Supplémentaires
            "matricule", "classroom", "enrollment_date", "parent_name", "parent_phone", "notes",
        ]
        widgets = {
            "birth_date": forms.DateInput(attrs={"type": "date"}),
            "enrollment_date": forms.DateInput(attrs={"type": "date"}),
            "notes": forms.Textarea(attrs={"rows": 3}),
        }
        labels = {
            "last_name": "Nom",
            "first_name": "Prénom",
            "birth_date": "Date de naissance",
            "city": "Ville",
            "district": "Quartier",
            "gender": "Genre",
            "photo": "Photo",
            "matricule": "Matricule",
            "classroom": "Classe",
            "enrollment_date": "Date d'inscription",
            "parent_name": "Nom du parent",
            "parent_phone": "N° Téléphone du parent",
            "notes": "Observation",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Champs obligatoires
        for name in ["last_name", "first_name", "birth_date", "city", "district", "gender"]:
            self.fields[name].required = True

        # Champs optionnels
        for name in ["photo", "matricule", "classroom", "enrollment_date", "parent_name", "parent_phone", "notes"]:
            self.fields[name].required = False

        if "classroom" in self.fields:
            self.fields["classroom"].empty_label = "— Sélectionner —"

        # Intitulés du genre (au cas où le modèle n’ait pas déjà les choices)
        if "gender" in self.fields:
            self.fields["gender"].choices = [("M", "Masculin"), ("F", "Féminin")]

    def clean_matricule(self):
        v = (self.cleaned_data.get("matricule") or "").strip()
        return v or None


# ===============================
# INSCRIPTION DES ANCIENS ÉLÈVES
# ===============================
class StudentEnrollOldForm(forms.Form):
    student = forms.ModelChoiceField(
        queryset=Student.objects.none(),
        label="Élève",
        help_text="Choisir un élève déjà existant (ancien élève)."
    )
    classroom = forms.ModelChoiceField(
        queryset=Classroom.objects.none(),
        label="Classe"
    )
    enrollment_date = forms.DateField(
        label="Date d'inscription",
        widget=forms.DateInput(attrs={"type": "date"})
    )
    notes = forms.CharField(
        label="Observation",
        widget=forms.Textarea(attrs={"rows": 3}),
        required=False
    )

    def __init__(self, *args, **kwargs):
        # Optionnel : permettre de filtrer par école active si tu fournis school_id
        school_id = kwargs.pop("school_id", None)
        super().__init__(*args, **kwargs)

        # Liste des élèves (tri par nom/prénom)
        qs_students = Student.objects.all().order_by("last_name", "first_name")
        # Student n’a plus forcément de champ school : on teste avant de filtrer
        if hasattr(Student, "school_id") and school_id:
            qs_students = qs_students.filter(school_id=school_id)
        self.fields["student"].queryset = qs_students

        # ✅ Correction ici : trier par cycle__name (pas cycle__label), puis par label de la classe
        qs_classes = Classroom.objects.all()
        if school_id:
            qs_classes = qs_classes.filter(school_id=school_id)
        qs_classes = qs_classes.select_related("cycle").order_by("cycle__name", "label")

        self.fields["classroom"].queryset = qs_classes
        self.fields["classroom"].empty_label = "— Sélectionner —"
