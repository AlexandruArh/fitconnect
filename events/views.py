from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Event, RSVP
from .forms import EventForm


def event_list(request):
    """Public list of all upcoming events."""
    events = Event.objects.filter(
        date_time__gt=__import__('django.utils.timezone', fromlist=['timezone']).timezone.now()
    ).order_by('date_time')
    return render(request, 'events/event_list.html', {'events': events})


def event_detail(request, pk):
    """Detail view for a single event."""
    from django.utils import timezone
    event = get_object_or_404(Event, pk=pk)
    user_rsvp = None
    if request.user.is_authenticated:
        user_rsvp = RSVP.objects.filter(user=request.user, event=event).first()
    return render(request, 'events/event_detail.html', {
        'event': event,
        'user_rsvp': user_rsvp,
    })


@login_required
def event_create(request):
    """Create a new event."""
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.organiser = request.user
            event.save()
            messages.success(request, f'Event "{event.title}" created successfully!')
            return redirect('events:detail', pk=event.pk)
    else:
        form = EventForm()
    return render(request, 'events/event_form.html', {'form': form, 'action': 'Create'})


@login_required
def event_edit(request, pk):
    """Edit an existing event (organiser only)."""
    event = get_object_or_404(Event, pk=pk, organiser=request.user)
    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            messages.success(request, 'Event updated successfully!')
            return redirect('events:detail', pk=event.pk)
    else:
        form = EventForm(instance=event)
    return render(request, 'events/event_form.html', {'form': form, 'action': 'Edit', 'event': event})


@login_required
def event_delete(request, pk):
    """Delete an event (organiser only)."""
    event = get_object_or_404(Event, pk=pk, organiser=request.user)
    if request.method == 'POST':
        title = event.title
        event.delete()
        messages.success(request, f'Event "{title}" deleted.')
        return redirect('events:list')
    return render(request, 'events/event_confirm_delete.html', {'event': event})


@login_required
def rsvp_toggle(request, pk):
    """Toggle RSVP status for an event (join or cancel)."""
    from django.utils import timezone
    event = get_object_or_404(Event, pk=pk)

    if not event.is_upcoming:
        messages.error(request, 'Cannot RSVP to a past event.')
        return redirect('events:detail', pk=pk)

    rsvp, created = RSVP.objects.get_or_create(user=request.user, event=event)

    if created or rsvp.status == 'cancelled':
        if event.is_full:
            messages.warning(request, 'Sorry, this event is full!')
        else:
            rsvp.status = 'confirmed'
            rsvp.save()
            messages.success(request, f'You have joined "{event.title}"!')
    else:
        rsvp.status = 'cancelled'
        rsvp.save()
        messages.info(request, f'You have cancelled your RSVP for "{event.title}".')

    return redirect('events:detail', pk=pk)
