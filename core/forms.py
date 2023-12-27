

from django import forms
from django.utils.html import format_html
from .models import *
class SearchCourierForm(forms.Form):
    tracking_id = forms.CharField(
        label='Tracking ID',
        max_length=255,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'tracking-input',
            'placeholder': 'Enter Tracking ID',
            'style': (
                'width: 100%; '
                'padding: 15px; '
                'border: 2px solid #3498db; '
                'border-radius: 25px; '
                'font-size: 16px; '
                'font-weight: bold; '
                'color: #333; '
                'background-color: #ecf0f1; '
                'transition: border-color 0.3s, background-color 0.3s; '
                'box-shadow: 0px 2px 6px rgba(0, 0, 0, 0.1); '
                'outline: none; '
            ),
        }),
    )

class SubscriberForm(forms.ModelForm):
    class Meta:
        model = Subscriber
        fields = ['mail']

    def __init__(self, *args, **kwargs):
        super(Subscriber, self).__init__(*args, **kwargs)

        placeholders = {
            'mail': 'Your Email',

            # Add more placeholders as needed
        }

        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control', 'placeholder': placeholders.get(field, '')})


