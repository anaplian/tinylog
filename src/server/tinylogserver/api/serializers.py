"""TinyLog API Serializers"""

from django.contrib.auth.models import User, Group
from rest_framework import serializers

from . import models


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email')


class TinyLogEntrySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.TinyLogEntry
        fields = ('url', 'owner', 'text_content', 'date_logged')


class TinyLogSerializer(serializers.HyperlinkedModelSerializer):
    log_entries = TinyLogEntrySerializer(many=True)

    class Meta:
        model = models.TinyLog
        fields = ('url', 'name', 'description', 'members', 'log_entries')
