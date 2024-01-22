from django.db import models

class DataTable3(models.Model):
    date = models.DateField()
    db_userid = models.IntegerField()
    db_importin = models.FloatField()
    db_importout = models.FloatField()
    db_exportin = models.FloatField()
    db_exportout = models.FloatField()
    db_transitin = models.FloatField()
    db_transitout = models.FloatField()
    db_exportempty = models.FloatField()
    db_otherempty = models.FloatField()
    db_unloadreid = models.FloatField()
    db_loadingreid = models.FloatField()
    db_lunloadport = models.FloatField()
    db_loadingport = models.FloatField()

