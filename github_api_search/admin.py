from django.contrib import admin

# Register your models here.
from .models import Users,Apicall

admin.site.register(Users)
admin.site.register(Apicall)