# Generated by Django 4.2.8 on 2024-01-24 13:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('firstapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ConstantUserData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('db_userid', models.IntegerField()),
                ('db_norms', models.IntegerField()),
                ('db_max', models.IntegerField()),
            ],
        ),
    ]
