from django.contrib import admin
from .models import Link
# Register your models here.
@admin.register(Link)
class AdminLink(admin.ModelAdmin):
    list_display=['short_code','original_url','created_at','hits']