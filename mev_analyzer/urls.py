from django.urls import path
from .views import MEVTransactionList, MEVTransactionDetail

urlpatterns = [
    path('mev/', MEVTransactionList.as_view(), name='mev-list'),
    path('mev/<str:tx_hash>/', MEVTransactionDetail.as_view(), name='mev-detail'),
]
