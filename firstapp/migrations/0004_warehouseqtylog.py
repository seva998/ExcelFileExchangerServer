# Generated by Django 5.0 on 2024-02-06 08:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('firstapp', '0003_dailymonitoringusercontainers_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='WarehouseQtyLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('db_userid', models.IntegerField()),
                ('date', models.DateField()),
                ('db_norms', models.IntegerField()),
                ('db_max', models.IntegerField()),
            ],
        ),
    ]