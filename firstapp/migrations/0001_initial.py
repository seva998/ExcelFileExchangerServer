# Generated by Django 4.2.8 on 2024-01-24 13:41

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DailyMonitoringUserData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('db_userid', models.IntegerField()),
                ('db_importin', models.IntegerField()),
                ('db_importout', models.IntegerField()),
                ('db_exportin', models.IntegerField()),
                ('db_exportout', models.IntegerField()),
                ('db_transitin', models.IntegerField()),
                ('db_transitout', models.IntegerField()),
                ('db_exportempty', models.IntegerField()),
                ('db_otherempty', models.IntegerField()),
                ('db_unload_reid_lin', models.IntegerField()),
                ('db_unload_reid_tramp', models.IntegerField()),
                ('db_loading_reid_lin', models.IntegerField()),
                ('db_loading_reid_tramp', models.IntegerField()),
                ('db_loading_port_lin', models.IntegerField()),
                ('db_loading_port_tramp', models.IntegerField()),
                ('db_unload_port_lin', models.IntegerField()),
                ('db_unload_port_tramp', models.IntegerField()),
                ('db_container_train', models.IntegerField()),
                ('db_container_auto', models.IntegerField()),
                ('db_container_auto_qty', models.IntegerField()),
                ('db_wagons', models.IntegerField()),
                ('db_wagons_out', models.IntegerField()),
                ('db_wagons_fe', models.IntegerField()),
                ('db_wagons_out_fe', models.IntegerField()),
                ('db_fittingplatform_in', models.IntegerField()),
                ('db_semiwagon_in', models.IntegerField()),
                ('db_auto_in', models.IntegerField()),
                ('db_sea_in', models.IntegerField()),
                ('db_fittingplatform_out', models.IntegerField()),
                ('db_semiwagon_out', models.IntegerField()),
                ('db_auto_out', models.IntegerField()),
                ('db_sea_out', models.IntegerField()),
                ('db_factload', models.IntegerField()),
                ('db_reload', models.IntegerField()),
            ],
        ),
    ]
