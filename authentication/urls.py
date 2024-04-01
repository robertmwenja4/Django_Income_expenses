from .views import RegistrationView, UsernameValidationView, EmailValidationView, VerificationView,LoginView, LogoutView, RequestPasswordResetEmail
from django.urls import path
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('register', RegistrationView.as_view(), name="register"),
    path('login', LoginView.as_view(), name="login"),
    path('reset-password', RequestPasswordResetEmail.as_view(), name="reset-password"),
    path('logout', LogoutView.as_view(), name="logout"),
    path('username-validation', csrf_exempt(UsernameValidationView.as_view()), name="username-validation"),
    path('email-validation', csrf_exempt(EmailValidationView.as_view()), name="email-validation"),
    path('activate/<uidb64>/<token>', VerificationView.as_view(), name="activate")
]
