from django.urls import path

from account.views import RegisterView, LoginView, MyTokenRefreshView

urlpatterns = [
    path('register', RegisterView.as_view(), name="register"),
    path('login', LoginView.as_view(), name='login'),
    path('refresh-token', MyTokenRefreshView.as_view(), name='refresh-token'),
]

