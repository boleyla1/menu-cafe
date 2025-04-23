from django.urls import path
from . import views
from .views import resend_otp

urlpatterns = [
    path('send-code/', views.UserLogin.as_view(), name='send_code'),
    path('verify-code/', views.ChekOtp.as_view(), name='verify_code'),
    path('nameuser/', views.CompleteProfileView.as_view(), name='nameuser'),
    path('otplogin/', views.OtpLoginView.as_view(), name='OtpLogin'),
    path('profile-update/', views.profile_update_view, name='profile_update'),
    path('logout/', views.logout_view, name='logout'),
    path('resend-otp/', resend_otp, name='resend_otp'),
]
