# Generated by Django 2.2 on 2019-04-29 19:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('vodaMainApp', '0003_auto_20190429_1938'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sources',
            name='city',
            field=models.ForeignKey(default=-1, on_delete=django.db.models.deletion.CASCADE, to='vodaMainApp.Cities'),
        ),
    ]