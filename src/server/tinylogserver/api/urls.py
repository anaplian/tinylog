"""TinyLog API URL Configuration"""

from django.conf.urls import include, url
from rest_framework import routers

from api import views


class APIRouter(routers.DefaultRouter):
    def __init__(self, allowed_prefixes, *args, **kwargs):
        self._allowed_prefixes = allowed_prefixes
        super(APIRouter, self).__init__(*args, **kwargs)

    def get_api_root_view(self, api_urls=None):
        """
        Return a basic root view.
        """
        api_root_dict = {}
        list_name = self.routes[0].name
        for prefix, viewset, basename in self.registry:
            if prefix in self._allowed_prefixes:
                api_root_dict[prefix] = list_name.format(basename=basename)

        return self.APIRootView.as_view(api_root_dict=api_root_dict)


router = APIRouter(('users', 'tiny-logs',))
router.register(r'users', views.UserViewSet)
router.register(r'tiny-logs', views.TinyLogViewSet)
router.register(r'tiny-log-entries', views.TinyLogEntryViewSet)


urlpatterns = [
    url(r'^', include(router.urls)),
]
