from django.urls import path
from rest_framework.routers import DefaultRouter
from content.views import ContentView
from content.Views.library_views import LibraryDetailView,LibraryView



urlpatterns = [
    path('content/new/', ContentView.as_view(), name="new_content"),
    path('library/', LibraryView.as_view(),name="library_views"),
    path('library/<int:pk>/',LibraryDetailView.as_view(),name= "library_detail")
]
