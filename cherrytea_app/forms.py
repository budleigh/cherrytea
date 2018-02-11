from django import forms
import pytz


class SigninForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())


class SignupForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())
    timezone = forms.ChoiceField(widget=forms.Select(), choices=((x, x) for x in pytz.all_timezones))


class PlanForm(forms.Form):
    day_of_week = forms.ChoiceField(widget=forms.Select(), choices=(
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
        ('Sunday', 'Sunday'),
    ))
    amount = forms.CharField(widget=forms.NumberInput())
    card = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Credit Card Number',
    }), required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['amount'].label = '$'
