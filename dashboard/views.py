from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils import timezone
from events.models import Event, RSVP


def home(request):
    """Public landing page."""
    upcoming = Event.objects.filter(date_time__gt=timezone.now()).order_by('date_time')[:6]
    return render(request, 'dashboard/home.html', {'upcoming_events': upcoming})


@login_required
def dashboard(request):
    """Authenticated user dashboard — my events and joined events."""
    now = timezone.now()

    # Events the user is organising (upcoming)
    my_events = Event.objects.filter(
        organiser=request.user,
        date_time__gt=now,
    ).order_by('date_time')

    # Events the user has joined (upcoming confirmed RSVPs)
    joined_rsvps = RSVP.objects.filter(
        user=request.user,
        status='confirmed',
        event__date_time__gt=now,
    ).select_related('event').order_by('event__date_time')

    joined_events = [rsvp.event for rsvp in joined_rsvps]

    # In-app notification: events happening within 24 hours
    soon = now + timezone.timedelta(hours=24)
    reminders = Event.objects.filter(
        date_time__gt=now,
        date_time__lte=soon,
        rsvps__user=request.user,
        rsvps__status='confirmed',
    ).distinct()

    return render(request, 'dashboard/dashboard.html', {
        'my_events': my_events,
        'joined_events': joined_events,
        'reminders': reminders,
    })
