from django.db.models import Count
from django.shortcuts import get_list_or_404

from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser as IsStaff
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Ticket
from .permissions import IsGroupSupportAndAuthenticated, IsGroupSalesAndAuthenticated
from .serializers import TicketSerializer
from .utils import add_sorting_if_exists


class TicketStatsViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    permission_classes = [IsStaff]

    @action(methods=['get'], detail=False)
    def get_stats(self, request):
        # total number of tickets
        ticket_number = Ticket.objects.count()

        # average number of images in a project
        nb_projects = len([item['project_name'] for item in list(Ticket.objects.values('project_name').distinct())])
        nb_images = sum([item['nb_images'] for item in list(Ticket.objects.values('nb_images'))])
        average_nb_images = nb_images / nb_projects

        # user with most closed tickets
        user_with_most_closed_tickets = list(
            Ticket.objects
            .filter(status='DONE')
            .values('owner__username')
            .annotate(total=Count('id'))
            .order_by('-total')
        )[0]

        return Response({
            'ticket_number': ticket_number,
            'median_nb_images': float(f'{average_nb_images:.2f}'),
            'user_with_most_closed_tickets': user_with_most_closed_tickets['owner__username'],
        })


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

    @action(methods=['get'], detail=False)
    def filter_by_support_user(self, request, user_name):
        """
        This endpoint returns all Ticket objects given an input User name.
        The filter only works on users belonging to the support team.
        """
        query_set = Ticket.objects.filter(owner__username=user_name, owner__groups__name__in=['team_support', 'team_sales'])
        query_set = add_sorting_if_exists(request, query_set, ['created_at', 'closed_at'])

        tickets = get_list_or_404(query_set)
        serializer = self.get_serializer(tickets, many=True)

        return Response(serializer.data)
