from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import *

urlpatterns = [
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/',UserRegisterApi.as_view(), name="user_register"),
    path('user-list/',UserListApi.as_view(), name="user_list"),
    path('fitness-classes/',FitnessClassApi.as_view(), name="fitness_classes"),
    path('booking/',BookingApi.as_view(), name="fitness_classes_booking"),
    path('booking-history/',BookingHistoryApi.as_view(), name="fitness_classes_booking_history"),
]