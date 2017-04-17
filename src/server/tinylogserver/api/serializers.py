"""TinyLog API Serializers"""

from rest_framework import serializers

from core import models as core_models


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = core_models.TinyLogUser
        fields = ('url', 'username', 'display_name', 'password')
        extra_kwargs = {
            'password': {'write_only': True},
        }


class TinyLogEntrySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = core_models.TinyLogEntry
        fields = ('url', 'created_by', 'text_content', 'date_logged')


class TinyLogSerializer(serializers.HyperlinkedModelSerializer):
    log_entries = TinyLogEntrySerializer(many=True)

    class Meta:
        model = core_models.TinyLog
        fields = ('url', 'name', 'description', 'members', 'log_entries')
