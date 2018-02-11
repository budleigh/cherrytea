from django import forms


class AuthForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())
    type = forms.ChoiceField(widget=forms.RadioSelect(), choices=(
        ('IN', 'Sign in'),
        ('UP', 'Sign up'),
    ))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['type'].label = ''


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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['amount'].label = '$'
