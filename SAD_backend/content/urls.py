from django.urls import path
from content.views import ContentView, LibraryView, AddContentToLibraryView, GetLibraryFiles, DownloadView

urlpatterns = [
    path('content/', ContentView.as_view(), name="view content"),
    path('library/', LibraryView.as_view(), name="view library"),
    path('add-content-to-library/', AddContentToLibraryView.as_view(), name="add content to library"),
    path('get-library-files/', GetLibraryFiles.as_view(), name="get library files"),
    path('download/<str:file_path>', DownloadView.as_view(), name='download view')
]
