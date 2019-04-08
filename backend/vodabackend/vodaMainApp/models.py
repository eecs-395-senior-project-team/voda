from django.db import models


# Create your models here.
class Cities(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=200)
    state_id = models.ForeignKey(State, on_delete=models.CASCADE)
    county_id = models.ForeignKey(Counties, on_delete=models.CASCADE)


class Counties(models.model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=200)
    state = models.ForeignKey(State, on_delete=models.CASCADE)


class State(models.Model):
    state_id = models.CharField(max_length=2, primary_key=True)


class Sources(models.Model):
    source_id = models.IntegerField(primary_key=True)
    utility_name = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    state = models.ForeignKey(State, on_delete=models.CASCADE)
    number_served = models.IntegerField()
    score = models.FloatField()
    # TODO: Add congressional information etc.


class Contaminants(models.Model):
    contaminant_id = models.IntegerField(primary_key=True)
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


class StateAvgLevels(models.Model):
    state_id = models.ForeignKey(State, on_delete=models.CASCADE)
    contaminant_id = models.ForeignKey(Contaminants, on_delete=models.CASCADE)
    state_avg = models.DecimalField(decimal_places=3, max_digits=10)
