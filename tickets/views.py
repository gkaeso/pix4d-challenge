from django.shortcuts import get_list_or_404

from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Ticket
from .permissions import IsGroupSupportAndAuthenticated, IsGroupSalesAndAuthenticated
from .serializers import TicketSerializer
from .utils import add_sorting_if_exists


class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    permission_classes = [IsGroupSupportAndAuthenticated | IsGroupSalesAndAuthenticated]

    @action(methods=['get'], detail=False)
    def filter_by_client(self, request, client_id):
        """
        This endpoint returns all Ticket objects given an input client ID.
        """
        query_set = Ticket.objects.filter(client=client_id)
        query_set = add_sorting_if_exists(request, query_set, ['created_at', 'closed_at'])

        tickets = get_list_or_404(query_set)
        serializer = self.get_serializer(tickets, many=True)

        return Response(serializer.data)
