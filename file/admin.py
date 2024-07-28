# admin.py
from django.contrib import admin
from .models import CSVfiles, CSVData

admin.site.register(CSVfiles)
admin.site.register(CSVData)
