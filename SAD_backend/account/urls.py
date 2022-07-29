from django.urls import path

from account.views import RegisterView, LoginView, MyTokenRefreshView, CheckUsernameView, GetUserInfoView

urlpatterns = [
    path('register', RegisterView.as_view(), name="register"),
    path('login', LoginView.as_view(), name='login'),
    path('refresh-token', MyTokenRefreshView.as_view(), name='refresh-token'),
    path('check-username', CheckUsernameView.as_view(), name='check-username'),
    path('get-info', GetUserInfoView.as_view(), name='get-info'),
]

