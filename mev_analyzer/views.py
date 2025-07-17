from rest_framework import generics
from .models import MEVTransaction
from .serializers import MEVTransactionSerializer
# This file defines the API views for MEV transactions in the HELIUS Analyzer application.
class MEVTransactionList(generics.ListAPIView):
    print("📡 Fetching MEV transactions...")
    serializer_class = MEVTransactionSerializer

    def get_queryset(self):
        queryset = MEVTransaction.objects.all().order_by('-timestamp')
        wallet = self.request.query_params.get('wallet')
        platform = self.request.query_params.get('platform')

        if wallet:
            queryset = queryset.filter(wallet__icontains=wallet)
        if platform:
            queryset = queryset.filter(platforms__icontains=platform)

        return queryset

# This view handles the retrieval of a list of MEV transactions, allowing for filtering by wallet and platform.
class MEVTransactionDetail(generics.RetrieveAPIView):
    queryset = MEVTransaction.objects.all()
    serializer_class = MEVTransactionSerializer
    lookup_field = 'tx_hash'
