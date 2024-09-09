from django.urls import path
from .views import GetEncryptionKeyView, DownloadFileView

urlpatterns = [
    path('download/<str:file_name>/', DownloadFileView.as_view(), name='download_file'),
    path('encryption_key/<str:file_name>/', GetEncryptionKeyView.as_view(), name='get_encryption_key'),
]