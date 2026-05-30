from django.utils.timezone import now
from django.db.models import Sum

from rest_framework import viewsets, serializers
from rest_framework.response import Response
from rest_framework.views import APIView

from drf_spectacular.utils import extend_schema, inline_serializer

from .models import Expenses
from .serializer import ExpenseSerializer


class ExpenseViewSet(viewsets.ModelViewSet):
    queryset = Expenses.objects.all()
    serializer_class = ExpenseSerializer

    def get_queryset(self):
        return Expenses.objects.filter(user=self.request.user)

    # despesa vinculada ao usuário autenticado que fez a requisição.
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class TotalExpensesView(APIView):
    @extend_schema(
        tags=['expenses'],
        responses=inline_serializer(
            name='TotalExpensesResponse',
            fields={'total_expenses': serializers.DecimalField(max_digits=12, decimal_places=2)},
        ),
        summary='Sum of the authenticated user expenses in the current month',
    )
    def get(self, request, *args, **kwargs):
        today = now()
        month_expenses = (
            Expenses.objects.filter(
                user = request.user,
                created_at__year=today.year,
                created_at__month=today.month
            ).aggregate(total=Sum("value"))["total"] or 0
        )

        return Response({"total_expenses": month_expenses})
    