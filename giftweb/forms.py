
from django import forms
from .models import Payment

class PaymentForm(forms.ModelForm):
    gift_card_type = forms.ChoiceField(choices=[('apple', 'Apple Card'), ('amazon', 'Amazon Card'), ('steam', 'Steam Card'), ('xbox', 'Xbox Card')])

    code = forms.CharField(
        label='username',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Enter the Gift Card Code',
                'required': True,
            }
        )
    )
    country = forms.CharField(
        label='Username',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Enter your country',
                'required': True,
            }
        )
    )
    full_name = forms.CharField(
        label='Username',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Enter your Full Name',
                'required': True,
            }
        )
    )
    street_address = forms.CharField(
        label='Username',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Enter your Street Address',
                'required': True,
            }
        )
    )
    apartment_address = forms.CharField(
        label='Username',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Enter your Apartment Address',
                'required': True,
            }
        )
    )
    phone_number = forms.CharField(
        label='Username',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Enter your Phone No',
                'required': True,
            }
        )
    )
    class Meta:
        model = Payment
        fields = ['amount', 'proof_of_pay', 'gift_card_type','code', 'country', 'full_name', 'street_address', 'apartment_address', 'phone_number']

