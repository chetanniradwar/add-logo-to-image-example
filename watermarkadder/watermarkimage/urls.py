from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import UserProfileViewSet, ImageViewSet, CustomTokenObtainPairView

router = DefaultRouter()
router.register(r'user-profile', UserProfileViewSet)
router.register(r'image', ImageViewSet)


urlpatterns = router.urls

urlpatterns += [
    path('user-login/', CustomTokenObtainPairView.as_view(),)
]

