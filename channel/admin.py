from django.contrib import admin
from .models import Channel, Member

@admin.register(Channel)
class ChannelAdmin(admin.ModelAdmin):
    pass

@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    pass