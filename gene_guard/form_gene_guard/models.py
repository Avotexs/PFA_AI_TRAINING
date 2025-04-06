from django.db import models

class Reponses_Sickle_Cell_Anemia(models.Model):
    CHOICES_YES_NO = [("yes", "Yes"), ("no", "No")]
    CHOICES_ORIGINS = [("African", "African"), ("Meditterranian", "Mediterranean"), ("Middle_East", "Middle East"), ("Other", "Other")]
    CHOICES_HEMOGLOBIN = [("HbA", "HbA"), ("HbS", "HbS"), ("Other", "Other")]

    oneforme1 = models.CharField(max_length=50, choices=CHOICES_YES_NO)
    twoforme1 = models.CharField(max_length=50, choices=CHOICES_YES_NO)
    threeforme1 = models.CharField(max_length=50, choices=CHOICES_YES_NO)
    fourforme1 = models.CharField(max_length=50, choices=CHOICES_ORIGINS)
    fiveforme1 = models.CharField(max_length=50, choices=CHOICES_YES_NO)
    sixforme1 = models.CharField(max_length=50, choices=CHOICES_YES_NO)
    sevenforme1 = models.CharField(max_length=50, choices=CHOICES_YES_NO)
    eightforme1 = models.CharField(max_length=50, choices=CHOICES_YES_NO)
    nineforme1 = models.CharField(max_length=50, choices=CHOICES_YES_NO)
    tenforme1 = models.CharField(max_length=50, choices=CHOICES_YES_NO)
    elevenforme1 = models.CharField(max_length=50, choices=CHOICES_HEMOGLOBIN)
    twelveforme1 = models.CharField(max_length=50, choices=CHOICES_YES_NO)
    thirteenforme1 = models.CharField(max_length=50, choices=CHOICES_YES_NO)
    fourteenforme1 = models.CharField(max_length=50, choices=CHOICES_YES_NO)
    fifteenforme1 = models.CharField(max_length=50, choices=CHOICES_YES_NO)




# hadi pour la base de donnees
class SickleCellResult(models.Model):
    user_id = models.AutoField(primary_key=True)  # ID unique
    responses = models.JSONField()  # Stocke les réponses sous forme JSON
    created_at = models.DateTimeField(auto_now_add=True)  # Date d'enregistrement

    def __str__(self):
        return f"Result ID: {self.user_id}"

