# =====================
# user_info/urls.py
# =====================
# =====================
# user_info/urls.py
# =====================

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserInformationViewSet,
    UserLoginView,
    UserDetailsByEmail
)

# Router setup for viewsets
router = DefaultRouter()
router.register(r'userinformation', UserInformationViewSet, basename='userinformation')

# Final combined urlpatterns
urlpatterns = [
    path('', include(router.urls)),  # /user_info/userinformation/
    path('login/', UserLoginView.as_view(), name='user-login'),  # /user_info/login/
    path('get_user_details/', UserDetailsByEmail.as_view(), name='get_user_details'),  # /user_info/get_user_details/
]
