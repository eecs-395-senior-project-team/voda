from django.db import models


# Create your models here.
class States(models.Model):
    state_id = models.CharField(max_length=2, primary_key=True)


class Counties(models.Model):
    id = models.CharField(max_length=5, primary_key=True)
    name = models.CharField(max_length=200)
    state = models.ForeignKey(States, on_delete=models.CASCADE)


class Cities(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    state = models.ForeignKey(States, on_delete=models.CASCADE)
    county = models.ForeignKey(Counties, on_delete=models.CASCADE)


class Sources(models.Model):
    source_id = models.AutoField(primary_key=True)
    utility_name = models.CharField(max_length=500)
    city = models.ForeignKey(Cities, on_delete=models.CASCADE, null=True)
    state = models.ForeignKey(States, on_delete=models.CASCADE, null=True)
    county = models.ForeignKey(Counties, on_delete=models.CASCADE, null=True)
    number_served = models.IntegerField()
    rating = models.FloatField(null=True)


class Contaminants(models.Model):
    contaminant_id = models.AutoField(primary_key=True)
    contaminant_name = models.CharField(max_length=200)
    health_guideline = models.DecimalField(decimal_places=3, max_digits=10, null=True)
    legal_limit = models.DecimalField(decimal_places=3, max_digits=10, null=True)
    national_avg = models.DecimalField(decimal_places=3, max_digits=10, null=True)
    summary = models.TextField(null=True)
    health_concerns = models.TextField(null=True)
    long_health_concerns = models.TextField(null=True)


class SourceLevels(models.Model):
    source = models.ForeignKey(Sources, on_delete=models.CASCADE)
    contaminant = models.ForeignKey(Contaminants, on_delete=models.CASCADE)
    contaminant_level = models.DecimalField(decimal_places=3, max_digits=10, null=True)


class StateAvgLevels(models.Model):
    state = models.ForeignKey(States, on_delete=models.CASCADE)
    contaminant = models.ForeignKey(Contaminants, on_delete=models.CASCADE)
    state_avg = models.DecimalField(decimal_places=3, max_digits=10, null=True)
