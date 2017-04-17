"""TinyLog API Views"""

from rest_framework import viewsets

from api import (
    serializers as api_serializers,
)
from core import (
    models as core_models,
)


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or created
    """
    queryset = core_models.TinyLogUser.objects.exclude(is_staff=1).order_by(
        '-date_joined')
    serializer_class = api_serializers.UserSerializer


class TinyLogViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows TinyLogs to be viewed or created
    """
    queryset = core_models.TinyLog.objects.all()
    serializer_class = api_serializers.TinyLogSerializer


class TinyLogEntryViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows TinyLogs to be viewed or created
    """
    queryset = core_models.TinyLogEntry.objects.all()
    serializer_class = api_serializers.TinyLogEntrySerializer
