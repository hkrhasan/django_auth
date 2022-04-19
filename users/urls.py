from django.urls import path, include

from users.views import UserProfileView, UserRegistrationView

urlpatterns = [
    path('login', UserRegistrationView.as_view(), name='login'),
    path('profile', UserProfileView.as_view(), name='profile'),
]


