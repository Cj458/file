from django.contrib import admin
from .models import File


@admin.register(File)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['file', 'uploaded_at', 'processed']

    list_per_page = 10
    list_filter = ['uploaded_at']
    search_fields = ['file__istartswith']

