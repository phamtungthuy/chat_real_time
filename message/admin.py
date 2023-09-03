from django.contrib import admin
from .models import Message, Emoji, Reaction

# Register your models here.

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    pass

@admin.register(Emoji)
class EmojiAdmin(admin.ModelAdmin):
    pass

@admin.register(Reaction)
class ReactionAdmin(admin.ModelAdmin):
    pass
