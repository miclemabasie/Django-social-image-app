from django.contrib import admin
from .models import Action

@admin.register(Action)
class ActionAdmin(admin.ModelAdmin):
    list_display = ['user', 'verb', 'target_id', 'target_content_type', 'created']
    list_filter = ('created',)
    search_fields = ('verb', )