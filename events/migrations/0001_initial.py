# Generated migration for FitConnect events app
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('category', models.CharField(
                    choices=[
                        ('running', 'Running Club'),
                        ('yoga', 'Yoga Class'),
                        ('hiking', 'Group Hike'),
                        ('cycling', 'Cycling'),
                        ('gym', 'Gym Session'),
                        ('other', 'Other'),
                    ],
                    default='other',
                    max_length=20,
                )),
                ('location', models.CharField(max_length=300)),
                ('date_time', models.DateTimeField()),
                ('max_participants', models.PositiveIntegerField(default=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('organiser', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='organised_events',
                    to=settings.AUTH_USER_MODEL,
                )),
            ],
            options={'ordering': ['date_time']},
        ),
        migrations.CreateModel(
            name='RSVP',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(
                    choices=[('confirmed', 'Confirmed'), ('cancelled', 'Cancelled')],
                    default='confirmed',
                    max_length=10,
                )),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('event', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='rsvps',
                    to='events.event',
                )),
                ('user', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='rsvps',
                    to=settings.AUTH_USER_MODEL,
                )),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='rsvp',
            unique_together={('user', 'event')},
        ),
    ]
