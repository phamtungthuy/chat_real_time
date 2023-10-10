from django.contrib import admin
from .models import Report

@admin.register(Report)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['id', 'report_type', 'processed', 'create_at']
