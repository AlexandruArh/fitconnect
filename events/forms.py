from django import forms
from .models import Event


class EventForm(forms.ModelForm):
    """Form for creating and editing FitConnect events."""

    class Meta:
        model = Event
        fields = ['title', 'description', 'category', 'location', 'date_time', 'max_participants']
        widgets = {
            'date_time': forms.DateTimeInput(
                attrs={'type': 'datetime-local'},
                format='%Y-%m-%dT%H:%M',
            ),
            'description': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields['date_time'].initial = self.instance.date_time.strftime('%Y-%m-%dT%H:%M')

    def clean_date_time(self):
        from django.utils import timezone
        dt = self.cleaned_data.get('date_time')
        if dt and dt <= timezone.now():
            raise forms.ValidationError('Event must be scheduled in the future.')
        return dt

    def clean_max_participants(self):
        value = self.cleaned_data.get('max_participants')
        if value is not None and value < 2:
            raise forms.ValidationError('An event must allow at least 2 participants.')
        return value
