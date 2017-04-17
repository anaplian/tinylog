from django.contrib import admin

from .models import TinyLog, TinyLogEntry, TinyLogUser

admin.site.register(TinyLog)
admin.site.register(TinyLogEntry)
admin.site.register(TinyLogUser)
