# users/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SomeServiceViewSet, RegisterView, LoginView, LogoutView

router = DefaultRouter()

urlpatterns = [
    path("", include(router.urls)),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path(
        "service/some_feature/",
        SomeServiceViewSet.as_view({"get": "some_feature"}),
        name="some_feature",
    ),
]
