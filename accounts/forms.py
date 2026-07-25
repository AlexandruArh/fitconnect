from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class RegisterForm(UserCreationForm):
    """Extended registration form with email field."""
    email = forms.EmailField(required=True, help_text='Required. Used for event reminders.')

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

   
    def save(self):
        try:
            user = User.objects.create_user(
                username=self.cleaned_data["username"],
                email=self.cleaned_data["email"],
                password=self.cleaned_data["password1"],
            )
            return user
        except IntegrityError:
            raise forms.ValidationError(
                "An account with this username already exists."
            )
class PersonalDetailsForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username", "email", "first_name", "last_name"]
        widgets = {
            "username": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "last_name": forms.TextInput(attrs={"class": "form-control"}),
        }

    def clean_email(self):
        email = self.cleaned_data["email"].strip().lower()
        qs = User.objects.filter(email__iexact=email).exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError("An account with this email already exists.")
        return email
