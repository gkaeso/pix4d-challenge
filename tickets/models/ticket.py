from django.contrib.auth import get_user_model
from django.db import models

from model_utils import Choices


class Ticket(models.Model):

    STATUSES = Choices(
        ('PENDING', 'Pending'),
        ('IN_PROGRESS', 'In Progress'),
        ('DONE', 'Done'),
    )

    owner = models.ForeignKey(get_user_model(), models.CASCADE, related_name='owned_tickets')
    client = models.ForeignKey(get_user_model(), models.CASCADE, related_name='raised_tickets')
    status = models.CharField(choices=STATUSES, null=True, blank=True, max_length=50)
    project_name = models.CharField(null=False, blank=False, max_length=100, db_index=True)
    nb_images = models.IntegerField(null=False, blank=False)
    created_at = models.DateTimeField(null=False, blank=False)
    closed_at = models.DateTimeField(null=True, blank=True)
    centered_at_lat = models.FloatField(null=True, blank=True)
    centered_at_lon = models.FloatField(null=True, blank=True)
    coordinate_system = models.CharField(null=False, blank=False, max_length=10)
    comments = models.TextField(null=True, blank=True)

    def __str__(self):
        return f'Ticket {self.id}'
