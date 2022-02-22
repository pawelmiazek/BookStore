from django.urls import include, path
from rest_framework import routers

from tasks.views import BookViewSet

router = routers.DefaultRouter()
router.register("books", BookViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
