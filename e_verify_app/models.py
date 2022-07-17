# My Django imports
from django.db import models
import uuid

# My app imports

class ResultInformation(models.Model):
    programme_select = (
        ('National Diploma', 'ND'),
        ('Higher National Diploma', 'HND'),
    )
    grade_select = (
        ('Pass', 'Pass'),
        ('Lower Credit', 'Lower Credit'),
        ('Upper Credit', 'Upper Credit'),
        ('Distinction', 'Distinction'),
    )
    fullname = models.CharField(max_length=100)
    programme = models.CharField(max_length=25, choices=programme_select)
    department = models.CharField(max_length=20)
    grade = models.CharField(max_length=20, choices=grade_select)
    cert_no = models.CharField(max_length=14, db_index=True, unique=True, blank=True)
    result_id = models.SlugField(default=uuid.uuid4(), primary_key=True, unique=True, editable=False)
    date = models.DateField()

    class Meta:
        db_table = 'Result Information'
        verbose_name_plural = 'Result Information'
