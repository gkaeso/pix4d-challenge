from datetime import datetime

from django.contrib.auth.models import User, Group
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from .models import Ticket


class TicketTest(APITestCase):

    @classmethod
    def setUpTestData(cls) -> None:
        sales_user = User.objects.create_user('sales_user', 'sales@test.com', 'password', is_staff=True, is_active=True)
        sales_group = Group.objects.create(name='team_sales')
        sales_group.user_set.add(sales_user)

        support_user = User.objects.create_user('support_user', 'support@test.com', 'password', is_staff=True, is_active=True)
        support_group = Group.objects.create(name='team_support')
        support_group.user_set.add(support_user)

        user = User.objects.create_user('user', 'user@test.com', 'password', is_staff=False, is_active=True)

        Ticket.objects.create(
            owner=sales_user,
            client=user,
            status='Pending',
            project_name='myproject',
            nb_images=1,
            created_at=datetime.today(),
            closed_at=datetime.now(),
            centered_at_lat=0,
            centered_at_lon=0,
            coordinate_system='0.00;0.00',
            comments='new comment'
        )

        Ticket.objects.create(
            owner=support_user,
            client=user,
            status='Pending',
            project_name='myproject',
            nb_images=1,
            created_at=datetime.today(),
            closed_at=datetime.now(),
            centered_at_lat=0,
            centered_at_lon=0,
            coordinate_system='0.00;0.00',
            comments='new comment'
        )

    def test_filter_by_support_user__not_logged_user(self):
        url = reverse('tickets-support', args=['sales_user'])
        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_filter_by_support_user__logged_user_is_not_support_team_or_not_sales_team(self):
        user = User.objects.get(username='user')
        self.client.force_login(user)

        url = reverse('tickets-support', args=[user.username])
        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_filter_by_support_user__logged_user_is_support_team(self):
        user = User.objects.get(username='support_user')
        self.client.force_login(user)

        url = reverse('tickets-support', args=[user.username])
        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_filter_by_support_user__logged_user_is_sales_team(self):
        user = User.objects.get(username='sales_user')
        self.client.force_login(user)

        url = reverse('tickets-support', args=[user.username])
        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_filter_by_support_user__logged_user_is_support_team_but_username_does_not_exist(self):
        user = User.objects.get(username='support_user')
        self.client.force_login(user)

        url = reverse('tickets-support', args=['not_a_user'])
        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_filter_by_support_user__logged_user_is_sales_team_but_username_does_not_exist(self):
        user = User.objects.get(username='sales_user')
        self.client.force_login(user)

        url = reverse('tickets-support', args=['not_a_user'])
        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
