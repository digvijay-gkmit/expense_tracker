from django.urls import path
from .views import *

urlpatterns = [
    path("signup/", UserSignupView.as_view(), name="signup"),
    path('verify-email/<str:token>/', VerifyEmailView.as_view(), name='verify-email'),
    path("login/", UserLoginView.as_view(), name="login"),
    path("logout/", UserLogoutView.as_view(), name="logout"),
    path("profile/<uuid:pk>/", UserDetailView.as_view(), name="user-manage"),
    path("profile/", UserDetailView.as_view(), name="user-manage"),
    path("change-password/", ChangePasswordView.as_view(), name="change-password"),
]

# path("test/", UserTestView.as_view(), name="test"),
# path('update/', UserUpdateView.as_view(), name='user-update'),
