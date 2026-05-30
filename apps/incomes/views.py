from django.utils.timezone import now
from django.db.models import Sum

from rest_framework import viewsets, serializers
from rest_framework.response import Response
from rest_framework.views import APIView

from drf_spectacular.utils import extend_schema, inline_serializer

from .models import Incomes
from .serializer import IncomeSerializer


class IncomeViewSet(viewsets.ModelViewSet):
    queryset = Incomes.objects.all()
    serializer_class = IncomeSerializer

    def get_queryset(self):
        return Incomes.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class TotalIncomesView(APIView):
    @extend_schema(
        tags=['incomes'],
        responses=inline_serializer(
            name='TotalIncomesResponse',
            fields={'total_incomes': serializers.DecimalField(max_digits=12, decimal_places=2)},
        ),
        summary='Sum of the authenticated user incomes in the current month',
    )
    def get(self, request, *args, **kwargs):
        today = now()
        month_incomes = (
            Incomes.objects.filter(
                user=request.user,
                created_at__year=today.year,
                created_at__month=today.month
            ).aggregate(total=Sum("value"))["total"] or 0
        )

        return Response({"total_incomes": month_incomes})