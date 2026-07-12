from django import forms
from .models import Event
from django.utils import timezone


class EventForm(forms.ModelForm):
    """Form for creating and editing events."""

    class Meta:
        model = Event
        fields = ['title', 'description', 'category', 'location', 'date_time', 'max_participants']
        widgets = {
            'date_time': forms.DateTimeInput(
                attrs={'type': 'datetime-local'},
                format='%Y-%m-%dT%H:%M'
            ),
            'description': forms.Textarea(attrs={'rows': 4}),
        }

    def clean_date_time(self):
        """Validate that event date is in the future."""
        dt = self.cleaned_data.get('date_time')
        if dt and dt <= timezone.now():
            raise forms.ValidationError('Event date must be in the future.')
        return dt
