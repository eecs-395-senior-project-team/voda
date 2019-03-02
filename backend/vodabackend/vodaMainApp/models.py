from django.db import models

# Create your models here.
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
    health_guideline = models.CharField(max_length=200)
    legal_limit = models.CharField(max_length=200)
    national_avg = models.DecimalField()
    summary = models.TextField()
    health_concerns = models.TextField()
    long_health_concerns = models.TextField()

class SourceLevels(models.Model):
    source_id = models.ForeignKey(Sources, on_delete=models.CASCADE)
    contaminant_id = models.ForeignKey(Contaminants, on_delete=models.CASCADE)
    contaminant_level = models.CharField(max_length=200)

class State(models.Model):
    state_id = models.CharField(max_length(2), primary_key=True)

class State_Avg_Levels(models.Model):
    state_id = models.ForeignKey(State, on_delete=models.CASCADE)
    contaminant_id = models.ForeignKey(Contaminants, on_delete=models.CASCADE)
    state_avg = models.DecimalField()
