from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from .models import Event, RSVP


class EventModelTest(TestCase):
    """Unit tests for the Event model."""

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.future_event = Event.objects.create(
            title='Morning Run',
            description='Easy 5k run around the park.',
            category='running',
            location='Hyde Park, London',
            date_time=timezone.now() + timedelta(days=7),
            max_participants=10,
            organiser=self.user,
        )

    def test_event_is_upcoming(self):
        """Event in the future should be marked as upcoming."""
        self.assertTrue(self.future_event.is_upcoming)

    def test_event_not_full_initially(self):
        """Newly created event with 0 RSVPs should not be full."""
        self.assertFalse(self.future_event.is_full)

    def test_participant_count_increments_on_rsvp(self):
        """Participant count should reflect confirmed RSVPs."""
        RSVP.objects.create(user=self.user, event=self.future_event, status='confirmed')
        self.assertEqual(self.future_event.participant_count, 1)


class EventViewTest(TestCase):
    """Acceptance tests for event views."""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.event = Event.objects.create(
            title='Yoga Session',
            description='Beginner-friendly yoga class.',
            category='yoga',
            location='Community Centre',
            date_time=timezone.now() + timedelta(days=3),
            max_participants=15,
            organiser=self.user,
        )

    def test_event_list_accessible(self):
        """Event list page should return 200 for unauthenticated users."""
        response = self.client.get('/events/')
        self.assertEqual(response.status_code, 200)

    def test_event_detail_accessible(self):
        """Event detail page should return 200."""
        response = self.client.get(f'/events/{self.event.pk}/')
        self.assertEqual(response.status_code, 200)

    def test_create_event_requires_login(self):
        """Creating an event should redirect unauthenticated users to login."""
        response = self.client.get('/events/create/')
        self.assertEqual(response.status_code, 302)
        self.assertIn('/accounts/login/', response['Location'])

    def test_rsvp_toggle(self):
        """Authenticated user should be able to RSVP to an event."""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(f'/events/{self.event.pk}/rsvp/')
        self.assertEqual(response.status_code, 302)
        rsvp = RSVP.objects.get(user=self.user, event=self.event)
        self.assertEqual(rsvp.status, 'confirmed')
