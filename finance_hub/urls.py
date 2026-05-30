import apps.balance
import apps.balance.views
import apps.expenses.views
from apps.users.views import register_user, login_user, logout_user, CustomTokenObtainPairView
import apps.users.urls
import apps.expenses.urls
import apps.incomes.urls

from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)


urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

    path('api/register/', register_user, name="register_user"),
    path('api/login/', login_user, name="login_user"),

    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/logout/', logout_user, name='logout'),
    
    path('api/', include(apps.users.urls)),
    path('api/', include(apps.expenses.urls)),
    path('api/', include(apps.incomes.urls)),

    path('api/incomes/month', apps.incomes.views.TotalIncomesView.as_view(), name="incomes_month"),
    path('api/expenses/month', apps.expenses.views.TotalExpensesView.as_view(), name="expenses_month"),
    path('api/balance/month/', apps.balance.views.TotalBalanceView.as_view(), name="balance_month"), 
    path('balance/', apps.balance.views.BalanceView.as_view(), name="balance"),

    path('api/balance/date/', apps.balance.views.FilterBalanceByDateView.as_view(), name="balance_date"),
    path('api/download/balance/date/', apps.balance.views.DownloadPdfByDateView.as_view(), name="download_balance_pdf")
]
