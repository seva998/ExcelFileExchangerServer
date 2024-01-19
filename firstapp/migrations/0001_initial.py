# Generated by Django 4.2.8 on 2024-01-16 13:30

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DataTable2',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('db_importin', models.TextField()),
                ('db_importout', models.TextField()),
                ('db_exportin', models.TextField()),
                ('db_exportout', models.TextField()),
                ('db_transitin', models.TextField()),
                ('db_transitout', models.TextField()),
                ('db_exportempty', models.TextField()),
                ('db_otherempty', models.TextField()),
                ('db_unloadreid', models.TextField()),
                ('db_loadingreid', models.TextField()),
                ('db_lunloadport', models.TextField()),
                ('db_loadingport', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='DataTable3',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('UserID', models.IntegerField()),
                ('db_importin', models.FloatField()),
                ('db_importout', models.FloatField()),
                ('db_exportin', models.FloatField()),
                ('db_exportout', models.FloatField()),
                ('db_transitin', models.FloatField()),
                ('db_transitout', models.FloatField()),
                ('db_exportempty', models.FloatField()),
                ('db_otherempty', models.FloatField()),
                ('db_unloadreid', models.FloatField()),
                ('db_loadingreid', models.FloatField()),
                ('db_lunloadport', models.FloatField()),
                ('db_loadingport', models.FloatField()),
            ],
        ),
    ]
