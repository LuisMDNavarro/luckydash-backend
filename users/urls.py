from django.urls import path

from users.views import TestView

urlpatterns = [
    path("test/", TestView.as_view(), name="test"),
]
