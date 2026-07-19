"""Management command to seed the database with sample FitConnect events."""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from events.models import Event, RSVP
import datetime


SAMPLE_EVENTS = [
    {
        'title': 'Wembley Morning Run',
        'description': 'A friendly 5K morning run through Wembley Park. All paces welcome — we run together and no one gets left behind. Bring water and wear comfortable shoes.',
        'category': 'running',
        'location': 'Wembley Park, London',
        'days_from_now': 2,
        'hour': 7,
        'max_participants': 30,
    },
    {
        'title': 'Sunrise Yoga in the Park',
        'description': 'Start your week with a calming 60-minute yoga session on the grass. Suitable for all levels. Bring your own mat. We finish with a short meditation.',
        'category': 'yoga',
        'location': 'Hyde Park, London',
        'days_from_now': 3,
        'hour': 8,
        'max_participants': 20,
    },
    {
        'title': 'Chiltern Hills Group Hike',
        'description': 'An 8-mile circular hike through the beautiful Chiltern Hills. Moderate difficulty. Stunning views and great company. Packed lunch recommended.',
        'category': 'hiking',
        'location': 'Chiltern Hills, Buckinghamshire',
        'days_from_now': 5,
        'hour': 9,
        'max_participants': 15,
    },
    {
        'title': 'Saturday Cycling Club',
        'description': 'A 25-mile road cycling loop around West London. Suitable for intermediate cyclists. Average pace around 16 mph. Helmets required.',
        'category': 'cycling',
        'location': 'Richmond Park, London',
        'days_from_now': 6,
        'hour': 8,
        'max_participants': 12,
    },
    {
        'title': 'HIIT & Core Gym Session',
        'description': 'A high-intensity interval training session followed by a 20-minute core workout. Suitable for intermediate fitness levels. Towel and water essential.',
        'category': 'gym',
        'location': 'PureGym Wembley, London',
        'days_from_now': 4,
        'hour': 18,
        'max_participants': 10,
    },
    {
        'title': 'Evening Yoga Flow',
        'description': 'Wind down after work with a relaxing vinyasa yoga flow. Focus on flexibility and breathing. All levels welcome. Mats provided.',
        'category': 'yoga',
        'location': 'Yoga Space Hackney, London',
        'days_from_now': 7,
        'hour': 19,
        'max_participants': 18,
    },
    {
        'title': 'Parkrun Social — Finsbury Park',
        'description': 'Join us for the weekly 5K parkrun at Finsbury Park, followed by coffee and a catch-up at the nearby café. Free to enter, just register at parkrun.org.uk first.',
        'category': 'running',
        'location': 'Finsbury Park, London',
        'days_from_now': 8,
        'hour': 9,
        'max_participants': 50,
    },
    {
        'title': 'Beginner Hiking Day — Box Hill',
        'description': 'A gentle 4-mile walk along the North Downs at Box Hill. Perfect for those new to hiking. Dog friendly. National Trust parking on site.',
        'category': 'hiking',
        'location': 'Box Hill, Surrey',
        'days_from_now': 10,
        'hour': 10,
        'max_participants': 20,
    },
]


class Command(BaseCommand):
    help = 'Seed the database with sample events for development and demonstration.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Delete all existing events before seeding.',
        )
        parser.add_argument(
            '--username',
            type=str,
            default=None,
            help='Username to assign as organiser (defaults to first superuser found).',
        )

    def handle(self, *args, **options):
        if options['clear']:
            count = Event.objects.count()
            Event.objects.all().delete()
            self.stdout.write(self.style.WARNING(f'Deleted {count} existing events.'))

        # Find organiser
        username = options['username']
        if username:
            try:
                organiser = User.objects.get(username=username)
            except User.DoesNotExist:
                self.stderr.write(self.style.ERROR(f'User "{username}" not found.'))
                return
        else:
            organiser = User.objects.filter(is_superuser=True).first()
            if not organiser:
                organiser = User.objects.first()
            if not organiser:
                self.stderr.write(self.style.ERROR(
                    'No users found. Run: python manage.py createsuperuser'
                ))
                return

        self.stdout.write(f'Creating events as organiser: {organiser.username}')

        created_count = 0
        for data in SAMPLE_EVENTS:
            event_dt = timezone.now().replace(
                hour=data['hour'], minute=0, second=0, microsecond=0
            ) + datetime.timedelta(days=data['days_from_now'])

            event, created = Event.objects.get_or_create(
                title=data['title'],
                defaults={
                    'description': data['description'],
                    'category': data['category'],
                    'location': data['location'],
                    'date_time': event_dt,
                    'max_participants': data['max_participants'],
                    'organiser': organiser,
                },
            )
            if created:
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f'  ✓ Created: {event.title}'))
            else:
                self.stdout.write(f'  – Already exists: {event.title}')

        self.stdout.write(self.style.SUCCESS(
            f'\nDone! {created_count} event(s) created. Visit http://127.0.0.1:8000/events/'
        ))
