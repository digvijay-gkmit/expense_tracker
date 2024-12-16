from django.urls import path
from .views import *

urlpatterns = [
    path("signup/", UserSignupView.as_view(), name="signup"),
    path("login/", UserLoginView.as_view(), name="login"),
    path("logout/", UserLogoutView.as_view(), name="logout"),
    # path("test/", UserTestView.as_view(), name="test"),
    path('update/', UserUpdateView.as_view(), name='user-update'),
    path('delete/', UserDeleteView.as_view(), name='user-delete'),
]
