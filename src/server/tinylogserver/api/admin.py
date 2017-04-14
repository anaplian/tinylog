from django.contrib import admin

from .models import TinyLog, TinyLogEntry

admin.site.register(TinyLog)
admin.site.register(TinyLogEntry)
