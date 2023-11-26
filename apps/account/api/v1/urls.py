from django.urls import path

from . import views

urlpatterns = [
    path('register/', views.AccountRegisterAPIView.as_view()),
    path('verify-email/', views.EmailVerificationAPIView.as_view()),
    path('login/', views.LoginAPIView.as_view()),
    path('reset-password/', views.ResetPasswordAPIView.as_view()),
    path('set-password-confirm/<str:uidb64>/<str:token>/', views.SetPasswordConfirmAPIView.as_view()),
    path('set-password-completed/', views.SetNewPasswordCompletedAPIView.as_view()),
    path('profile/<str:email>/', views.MyAccountAPIView.as_view()),

]