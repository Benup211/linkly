from django.contrib import admin
from .models import customUser
# Register your models here.
@admin.register(customUser)
class AdmincustomUser(admin.ModelAdmin):
    list_display=['id','email','is_active']
