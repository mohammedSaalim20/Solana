from rest_framework import serializers
from .models import MEVTransaction


class MEVTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = MEVTransaction
        fields = '__all__'
