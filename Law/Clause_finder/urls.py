from django.urls import path
from .views import AnalyzeDocumentView,ListAnalyzedDocumentsView,RetrieveAnalyzedDocumentView

urlpatterns = [
    path('analyze/', AnalyzeDocumentView.as_view(), name='analyze-document'),
    path('responses/', ListAnalyzedDocumentsView.as_view(), name='view-all-responses'),
    path('responses/<int:pk>/', RetrieveAnalyzedDocumentView.as_view(), name='view-single-response'),
]