from django.db import models

# Create your models here.
class State(models.Model):
    state_id = models.CharField(max_length=2, primary_key=True)

class Sources(models.Model):
    source_id = models.AutoField(primary_key=True)
    utility_name = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    state = models.ForeignKey(State, on_delete=models.CASCADE)
    number_served = models.IntegerField()
    # TODO: Add congressional information etc.

class Contaminants(models.Model):
    contaminant_id = models.AutoField(primary_key=True)
    contaminant_name = models.CharField(max_length=200)
    health_guideline = models.DecimalField(decimal_places=3, max_digits=10)
    legal_limit = models.DecimalField(decimal_places=3, max_digits=10)
    national_avg = models.DecimalField(decimal_places=3, max_digits=10)
    summary = models.TextField()
    health_concerns = models.TextField()
    long_health_concerns = models.TextField()

class SourceLevels(models.Model):
    source_id = models.ForeignKey(Sources, on_delete=models.CASCADE)
    contaminant_id = models.ForeignKey(Contaminants, on_delete=models.CASCADE)
    contaminant_level = models.DecimalField(decimal_places=3, max_digits=10)

class State_Avg_Levels(models.Model):
    state_id = models.ForeignKey(State, on_delete=models.CASCADE)
    contaminant_id = models.ForeignKey(Contaminants, on_delete=models.CASCADE)
    state_avg = models.DecimalField(decimal_places=3, max_digits=10)
