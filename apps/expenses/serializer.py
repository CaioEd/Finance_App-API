from rest_framework import serializers
from .models import Expenses

class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expenses
        exclude = ['user']  # evita que o campo seja enviado pelo cliente.

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user # associa o user autenticado.
        return super().create(validated_data)