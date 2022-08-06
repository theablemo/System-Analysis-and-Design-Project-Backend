from django.urls import path

from base.views import ContentView

urlpatterns = [
    path('content/new/', ContentView.as_view(), name="new_content"),
    path('<str:library>/<str:filename>/', ContentView.as_view(), name='download_content')

]
