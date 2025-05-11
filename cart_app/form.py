from django import forms
from .models import Address

class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['address']
        widgets = {
            'address': forms.Textarea(attrs={'placeholder': 'آدرس خود را وارد کنید'})
        }
