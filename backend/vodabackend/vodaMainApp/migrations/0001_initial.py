# Generated by Django 2.0.10 on 2019-02-23 02:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Contaminants',
            fields=[
                ('contaminant_id', models.IntegerField(primary_key=True, serialize=False)),
                ('maximum_level', models.CharField(max_length=200)),
                ('associated_conditions', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='SourceLevels',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contaminant_level', models.CharField(max_length=200)),
                ('contaminant_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vodaMainApp.Contaminants')),
            ],
        ),
        migrations.CreateModel(
            name='Sources',
            fields=[
                ('source_id', models.IntegerField(primary_key=True, serialize=False)),
                ('city', models.CharField(max_length=200)),
                ('county', models.CharField(max_length=200)),
                ('state', models.CharField(max_length=200)),
                ('zipcode', models.CharField(max_length=5)),
                ('rating', models.DecimalField(decimal_places=1, max_digits=3)),
            ],
        ),
        migrations.AddField(
            model_name='sourcelevels',
            name='source_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vodaMainApp.Sources'),
        ),
    ]
