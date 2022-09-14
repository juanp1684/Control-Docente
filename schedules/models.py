from django.db import models
from django.contrib.auth.hashers import make_password
from .choices import DAY_CHOICES

# Create your models here.


class User(models.Model):
    codsis = models.CharField(max_length=10, primary_key=True)
    full_name = models.CharField(max_length=50)
    faculty = models.CharField(max_length=50)# later could be changed to a stringSet()
    contact_mail = models.CharField(max_length=60)
    last_connection = models.DateTimeField()
    password = models.CharField(max_length=255, null=True)

    def save(self, **kwargs):
        self.password = make_password(self.password)
        super().save(**kwargs)

    class Meta:
        db_table = 'user'


class Schedule(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, to_field="codsis")
    start_time = models.TimeField()
    end_time = models.TimeField()
    day_of_week = models.PositiveSmallIntegerField(choices=DAY_CHOICES)
    subject = models.CharField(max_length=200, null=True)

    class Meta:
        db_table = 'schedule'


class Report(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, to_field="codsis")
    schedule = models.ForeignKey(Schedule, on_delete=models.DO_NOTHING, to_field="id")
    report_time = models.DateTimeField()
    attempts = models.PositiveSmallIntegerField()
    report_type = models.CharField(max_length=30)# later could be changed to a stringSet ("Succesful", "Failed", "Missed", "Excused")

    class Meta:
        db_table = 'report'
