from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Event(models.Model):
    """Represents a fitness meetup or wellness event."""

    CATEGORY_CHOICES = [
        ('running', 'Running Club'),
        ('yoga', 'Yoga Class'),
        ('hiking', 'Group Hike'),
        ('cycling', 'Cycling'),
        ('gym', 'Gym Session'),
        ('other', 'Other'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='other')
    location = models.CharField(max_length=300)
    date_time = models.DateTimeField()
    max_participants = models.PositiveIntegerField(default=20)
    organiser = models.ForeignKey(User, on_delete=models.CASCADE, related_name='organised_events')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['date_time']

    def __str__(self):
        return f'{self.title} - {self.date_time.strftime("%d %b %Y %H:%M")}'

    @property
    def is_upcoming(self):
        """Returns True if the event hasn't happened yet."""
        return self.date_time > timezone.now()

    @property
    def participant_count(self):
        """Returns number of confirmed RSVPs."""
        return self.rsvps.filter(status='confirmed').count()

    @property
    def is_full(self):
        """Returns True if event has reached max participants."""
        return self.participant_count >= self.max_participants


class RSVP(models.Model):
    """Tracks a user's RSVP status for an event."""

    STATUS_CHOICES = [
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rsvps')
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='rsvps')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='confirmed')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'event')  # One RSVP per user per event

    def __str__(self):
        return f'{self.user.username} -> {self.event.title} ({self.status})'
