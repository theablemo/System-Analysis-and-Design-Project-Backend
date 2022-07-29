from django.urls import path
from account.views import RegisterView, LoginView, MyTokenRefreshView, CheckUsernameView, GetUserInfoView
from account.views.view_verify import VerifyView
from account.views.view_change_password import ChangePasswordView
from account.views.view_reset_password import ResetPasswordView

urlpatterns = [
    path('register', RegisterView.as_view(), name="register"),
    path('login', LoginView.as_view(), name='login'),
    path('refresh-token', MyTokenRefreshView.as_view(), name='refresh-token'),
    path('check-username', CheckUsernameView.as_view(), name='check-username'),
    path('get-info', GetUserInfoView.as_view(), name='get-info'),
    path('verify-account', VerifyView.as_view(), name="verify-account"),
    path('change-password', ChangePasswordView.as_view(), name="change-password"),
    path('reset-password', ResetPasswordView.as_view(), name="reset password")
]
