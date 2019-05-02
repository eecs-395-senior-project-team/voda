# Generated by Django 2.2.1 on 2019-05-02 02:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('vodaMainApp', '0003_auto_20190501_2327'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sources',
            name='city',
            field=models.ForeignKey(db_column='city_id', null=True, on_delete=django.db.models.deletion.CASCADE, to='vodaMainApp.Cities'),
        ),
        migrations.AlterField(
            model_name='sources',
            name='county',
            field=models.ForeignKey(db_column='county_id', null=True, on_delete=django.db.models.deletion.CASCADE, to='vodaMainApp.Counties'),
        ),
        migrations.AlterField(
            model_name='sources',
            name='state',
            field=models.ForeignKey(db_column='state_id', null=True, on_delete=django.db.models.deletion.CASCADE, to='vodaMainApp.States'),
        ),
        migrations.AlterField(
            model_name='sources',
            name='utility_name',
            field=models.CharField(max_length=200),
        ),
    ]