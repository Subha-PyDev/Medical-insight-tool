from django.urls import path
from .views import (
    DocumentUploadView,
    DocumentListView,
    DocumentQueryView,
    DocumentDeleteView
)

urlpatterns = [
    path('upload/', DocumentUploadView.as_view(), name='document-upload'),
    path('list/', DocumentListView.as_view(), name='document-list'),
    path('query/', DocumentQueryView.as_view(), name='document-query'),
    path('delete/<int:id>/', DocumentDeleteView.as_view(), name='document-delete'),
]
