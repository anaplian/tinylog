"""TinyLog API Views"""

from django.contrib.auth.models import User, Group
from rest_framework import viewsets

from api import models, permissions, serializers


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or created
    """
    queryset = User.objects.exclude(is_staff=1).order_by('-date_joined')
    serializer_class = serializers.UserSerializer
    permission_classes = (
        permissions.IsOwnerOrAdminOrReadOnly,
    )


class TinyLogViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows TinyLogs to be viewed or created
    """
    queryset = models.TinyLog.objects.all()
    serializer_class = serializers.TinyLogSerializer
    permission_classes = (
        permissions.IsOwnerOrAdminOrReadOnly,
    )


class TinyLogEntryViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows TinyLogs to be viewed or created
    """
    queryset = models.TinyLogEntry.objects.all()
    serializer_class = serializers.TinyLogEntrySerializer
    permission_classes = (
        permissions.IsOwnerOrAdminOrReadOnly,
    )
