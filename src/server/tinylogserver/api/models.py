"""TinyLog Models"""

from django.contrib.auth.models import User
from django.db import models


class TinyLog(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    members = models.ManyToManyField(User)

    def __str__(self):
        return 'TinyLog(id={}, name={})'.format(self.id, self.name)

    @property
    def log_entries(self):
        return [entry
            for entry in TinyLogEntry.objects.filter(tiny_log=self).\
                order_by('-date_logged')]


class TinyLogEntry(models.Model):
    tiny_log = models.ForeignKey(TinyLog, on_delete=models.CASCADE)
    owner = models.ForeignKey(User)
    text_content = models.CharField(max_length=500)
    date_logged = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return 'TinyLogEntry(parent_id={}, text_content={})'.format(
            self.tiny_log.id, self.text_content)
