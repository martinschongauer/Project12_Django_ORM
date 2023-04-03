from django.contrib import admin
from django.urls import path
from api.views import views_clients, views_contracts, views_events, views_teams
from rest_framework_simplejwt import views as jwt_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('managers/', views_teams.managers, name='managers'),
    path('managers/<int:manager_id>/', views_teams.managers_detail, name='managers_detail'),
    path('sales/', views_teams.sales, name='sales'),
    path('sales/<int:seller_id>/', views_teams.sales_detail, name='sales_detail'),
    path('support/', views_teams.support, name='support'),
    path('support/<int:support_id>/', views_teams.support_detail, name='support_detail'),
    path('clients/', views_clients.clients, name='clients'),
    path('clients/<int:client_id>/', views_clients.client_detail, name='client_detail'),
    path('contracts/', views_contracts.contracts, name='contract'),
    path('contracts/<int:contract_id>/', views_contracts.contract_detail, name='contract_detail'),
    path('events/', views_events.events, name='event'),
    path('events/<int:event_id>/', views_events.event_detail, name='event_detail'),
]
