from django.contrib import admin
from .models import AdminUser, Schedule, User, Report

# Register your models here.

admin.site.register(Schedule)
admin.site.register(User)
admin.site.register(Report)
admin.site.register(AdminUser)
