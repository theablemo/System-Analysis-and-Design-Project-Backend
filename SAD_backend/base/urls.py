from django.urls import path

from base.views import ContentView, ContentListView

urlpatterns = [
    path('content/new/', ContentView.as_view(), name="new_content"),
    path('content/all/', ContentListView.as_view(), name='all_contents'),
    path('download/<str:library>/<str:filename>/', ContentView.as_view(), name='download_content'),

]
