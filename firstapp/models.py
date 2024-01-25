from django.db import models

class DailyMonitoringUserData(models.Model):
    date = models.DateField()
    db_userid = models.IntegerField()

    #1 table

    db_importin = models.IntegerField()
    db_importout = models.IntegerField()
    db_exportin = models.IntegerField()
    db_exportout = models.IntegerField()
    db_transitin = models.IntegerField()
    db_transitout = models.IntegerField()
    db_exportempty = models.IntegerField()
    db_otherempty = models.IntegerField()
    db_unload_reid_lin = models.IntegerField()
    db_unload_reid_tramp = models.IntegerField()
    db_loading_reid_lin = models.IntegerField()
    db_loading_reid_tramp = models.IntegerField()
    db_loading_port_lin = models.IntegerField()
    db_loading_port_tramp = models.IntegerField()
    db_unload_port_lin = models.IntegerField()
    db_unload_port_tramp = models.IntegerField()


class DailyMonitoringUserContainers(models.Model):
    date = models.DateField()
    db_userid = models.IntegerField()
    #2 table

    db_container_train = models.IntegerField()
    db_container_auto = models.IntegerField()
    db_container_auto_qty = models.IntegerField()

class DailyMonitoringUserWagons(models.Model):
    date = models.DateField()
    db_userid = models.IntegerField()
    #3 table

    db_wagons = models.IntegerField()
    db_wagons_out = models.IntegerField()

class DailyMonitoringUserWagonsFE(models.Model):
    date = models.DateField()
    db_userid = models.IntegerField()
    #4 table

    db_wagons_fe = models.IntegerField()
    db_wagons_out_fe = models.IntegerField()

class DailyMonitoringUserTransport(models.Model):
    date = models.DateField()
    db_userid = models.IntegerField()
    #5 table & 6 table

    db_fittingplatform_in = models.IntegerField()
    db_semiwagon_in = models.IntegerField()
    db_auto_in = models.IntegerField()
    db_sea_in = models.IntegerField()           # only in 5 table
    db_fittingplatform_out = models.IntegerField()
    db_semiwagon_out = models.IntegerField()
    db_auto_out = models.IntegerField()
    db_sea_out = models.IntegerField()          # only in 5 table
    db_factload = models.IntegerField()         # only in 6 table
    db_reload = models.IntegerField()           # only in 6 table


class ConstantUserData(models.Model):
    db_userid = models.IntegerField()
    db_norms = models.IntegerField()
    db_max = models.IntegerField()



