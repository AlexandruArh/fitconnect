from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from events.models import Event, RSVP


def home(request):
    """Public home page - redirect logged-in users to dashboard."""
    if request.user.is_authenticated:
        return redirect('dashboard:index')
    upcoming = Event.objects.filter(date_time__gt=timezone.now()).order_by('date_time')[:6]
    return render(request, 'dashboard/home.html', {'upcoming_events': upcoming})


@login_required
def dashboard_index(request):
    """Main user dashboard showing upcoming sessions and RSVPs."""
    now = timezone.now()

    # Events the user has RSVP'd to (upcoming only)
    my_rsvps = RSVP.objects.filter(
        user=request.user,
        status='confirmed',
        event__date_time__gt=now
    ).select_related('event').order_by('event__date_time')

    # Events the user organised (upcoming only)
    my_events = Event.objects.filter(
        organiser=request.user,
        date_time__gt=now
    ).order_by('date_time')

    # All upcoming events (excluding those the user organised)
    discover = Event.objects.filter(
        date_time__gt=now
    ).exclude(organiser=request.user).order_by('date_time')[:10]

    return render(request, 'dashboard/dashboard.html', {
        'my_rsvps': my_rsvps,
        'my_events': my_events,
        'discover': discover,
    })
