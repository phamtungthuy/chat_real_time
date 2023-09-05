from django.contrib import admin
from .models import Channel, Member

@admin.register(Channel)
class ChannelAdmin(admin.ModelAdmin):
    list_display = ['id', 'title']

@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'channel']