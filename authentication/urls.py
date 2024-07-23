from django.urls import path
from .views import UserLoginView, UserLogoutView, ValidateSessionToken, ContinueSession

app_name = 'authentication'

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('api/validate-token/', ValidateSessionToken.as_view(), name='validate_token'),
    path('api/continue-session/', ContinueSession.as_view(), name='continue_session'),
]
