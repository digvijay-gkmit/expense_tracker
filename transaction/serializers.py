from rest_framework import serializers
from .models import Transaction

class TransactionSerializer(serializers.ModelSerializer):
    date = serializers.DateField(required=False)  
    class Meta:
        model = Transaction
        fields = '__all__'
    def create(self, validated_data):
        # Get the user from the request context
        request = self.context.get('request')
        if request:
            user = request.user  # Get the logged-in user
            validated_data['user'] = user
        return super().create(validated_data)
