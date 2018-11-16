# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models



class Course(models.Model):
    id = models.AutoField(primary_key=True)
    cid = models.CharField(max_length=30)
    cname = models.CharField(max_length=300)
    credits = models.FloatField()
    campus = models.CharField(max_length=150)
    department = models.CharField(max_length=160)
    term = models.CharField(max_length=150)
    division = models.CharField(max_length=200)
    prerequisites = models.CharField(max_length=1000, blank=True, null=True)
    exclusion = models.CharField(max_length=1000, blank=True, null=True)
    br = models.CharField(max_length=200, blank=True, null=True)
    lecnum = models.CharField(max_length=30, blank=True, null=True)
    lectime = models.CharField(max_length=125, blank=True, null=True)
    instructor = models.CharField(max_length=500, blank=True, null=True)
    location = models.CharField(max_length=250, blank=True, null=True)
    size = models.IntegerField(blank=True, null=True)
    currentenrollment = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'course'
        unique_together = (('cid', 'id'),)



