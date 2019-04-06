from django.contrib import admin

# Register your models here.

from .models import BerthType, Coach, TicketStatus, PassangerDetail, TicketDetail


# Minimal registration of Models.
admin.site.register(BerthType)
admin.site.register(Coach)
admin.site.register(TicketStatus)
admin.site.register(PassangerDetail)
admin.site.register(TicketDetail)
