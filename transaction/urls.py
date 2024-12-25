# transactions/urls.py
from django.urls import path
from .views import (
    TransactionView,
    TransactionSummaryView,
    # CategoryTransactionSummaryView
)

urlpatterns = [
    path("", TransactionView.as_view(), name="transaction-list-create"),
    path("<uuid:pk>/", TransactionView.as_view(), name="transaction-detail"),
    path("summary/", TransactionSummaryView.as_view(), name="transaction-summary"),
    #    path('transactions/category/<uuid:category_uuid>/', CategoryTransactionSummaryView.as_view(), name='category-transaction-summary')
]
