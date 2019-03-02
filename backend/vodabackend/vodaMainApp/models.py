from django.db import models


# Create your models here.
class Sources(models.Model):
    source_id = models.IntegerField(primary_key=True)
    city = models.CharField(max_length=200)
    county = models.CharField(max_length=200)
    state = models.CharField(max_length=200)
    zipcode = models.CharField(max_length=5)
    rating = models.DecimalField(max_digits=3, decimal_places=1)
    # TODO: Add congressional information etc.


class Contaminants(models.Model):
    contaminant_id = models.IntegerField(primary_key=True)
    maximum_level = models.CharField(max_length=200)
    associated_conditions = models.TextField()


class SourceLevels(models.Model):
    source_id = models.ForeignKey(Sources, on_delete=models.CASCADE)
    contaminant_id = models.ForeignKey(Contaminants, on_delete=models.CASCADE)
    contaminant_level = models.CharField(max_length=200)
