from rest_framework import serializers
from .models import Transaction

class TransactionSerializer(serializers.ModelSerializer):
    date = serializers.DateField(required=False)  
    class Meta:
        model = Transaction
        fields = '__all__'
        read_only_fields = ['id','created_at', 'updated_at']

    
    def validate_amount(self, amount):
        if amount <= 0:
            raise serializers.ValidationError("Amount must be greater than zero")
        max_amount = 9999999.99
        if amount >= max_amount:
            raise serializers.ValidationError("Amount must be greater than zero")
        return amount