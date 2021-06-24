from django.urls import include, path

from rest_framework import routers

from . import views


router = routers.DefaultRouter()
router.register('all', views.TicketViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('client/<int:client_id>', views.TicketViewSet.as_view({'get': 'filter_by_client'}), name='tickets-client'),
    path('support/<str:user_name>', views.TicketViewSet.as_view({'get': 'filter_by_support_user'}), name='tickets-support'),
    path('stats/', views.TicketStatsViewSet.as_view({'get': 'get_stats'})),
]
