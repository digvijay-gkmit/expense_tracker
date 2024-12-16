# transactions/urls.py
from django.urls import path
from .views import (
    TransactionListCreateView,
    TransactionDetailView,
    TransactionSummaryView,
    CategoryTransactionSummaryView
)

urlpatterns = [
    path('transactions/', TransactionListCreateView.as_view(), name='transaction-list-create'),
    path('transactions/<uuid:pk>/', TransactionDetailView.as_view(), name='transaction-detail'),
    path('transactions/summary/', TransactionSummaryView.as_view(), name='transaction-summary'),
    path('transactions/category/<uuid:category_uuid>/', CategoryTransactionSummaryView.as_view(), name='category-transaction-summary')
]