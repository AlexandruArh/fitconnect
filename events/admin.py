from django.contrib import admin
from .models import Event, RSVP


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'date_time', 'organiser', 'participant_count', 'is_full']
    list_filter = ['category', 'date_time']
    search_fields = ['title', 'location', 'organiser__username']


@admin.register(RSVP)
class RSVPAdmin(admin.ModelAdmin):
    list_display = ['user', 'event', 'status', 'created_at']
    list_filter = ['status']
