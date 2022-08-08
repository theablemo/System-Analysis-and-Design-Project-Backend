from django.urls import path

from content.views import ContentView

urlpatterns = [
    path('content/new/', ContentView.as_view(), name="new_content"),

]
