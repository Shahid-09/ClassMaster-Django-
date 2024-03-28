from django.contrib import admin
from .models import UserMaster, CourseMaster

# Register your models here.
admin.site.register(UserMaster)
admin.site.register(CourseMaster)