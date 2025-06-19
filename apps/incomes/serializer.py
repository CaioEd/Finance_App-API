from rest_framework import serializers
from .models import Incomes

class IncomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Incomes
        exclude = ['user']

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
