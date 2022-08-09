from django.urls import path
from rest_framework.routers import DefaultRouter
from content.views import ContentView
from content.views.library_views import *

# router = DefaultRouter()

# router.register("library",LibraryViewSet,"library_vs")


urlpatterns = [
    path('content/new/', ContentView.as_view(), name="new_content"),
    path('library/', LibraryView.as_view(),name="library_views"),
    path('library/<int:id>/',LibraryDetailView.as_view(),name= "library_detail")
]


# urlpatterns += router.urls
