from django.contrib import admin

from .models import Ticket


class TicketAdmin(admin.ModelAdmin):
    model = Ticket
    search_fields = ('id', 'owner', 'client', 'project_name')
    list_display = ('id', 'owner', 'client', 'project_name', 'created_at')


# Register your models here.
admin.site.register(Ticket, TicketAdmin)
