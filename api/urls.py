from django.urls import path
from .views import GetDecryptionKeyView, DownloadFileView

urlpatterns = [
    path('download/<str:file_name>/', DownloadFileView.as_view(), name='download_file'),
    path('decryption_key/<str:file_name>/', GetDecryptionKeyView.as_view(), name='get_decryption_key'),
]