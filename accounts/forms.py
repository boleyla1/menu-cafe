from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError
from django import forms
from .models import Otp
from django.utils.timezone import now
from datetime import timedelta

from .models import User


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""

    password1 = forms.CharField(label="رمز ورود", widget=forms.PasswordInput)
    password2 = forms.CharField(
        label="تکرار رمز ورود", widget=forms.PasswordInput
    )

    class Meta:
        model = User
        fields = ["phone", ]

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    disabled password hash display field.
    """

    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ["phone", "password", "is_active", "is_admin"]


class LogimForm(forms.Form):
    phone = forms.CharField(max_length=11, widget=forms.TextInput(attrs={'class': 'form-control'}))

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if len(phone) > 11:
            raise ValidationError(
                "شماره متعبر نیست: %(value)s",
                code="invalid",
                params={"value": f"{phone}"},
            )
        return phone


class RegisterForm(forms.Form):
    phone = forms.CharField(max_length=11, widget=forms.TextInput(attrs={'class': 'form-control'}))


class ChekOtpForm(forms.Form):
    code = forms.CharField(
        max_length=4,
        min_length=4,
        required=True,
        error_messages={
            'required': 'لطفاً کد تأیید را وارد کنید.',
            'max_length': 'کد باید دقیقا ً 4 رقم باشد.',
            'min_length': 'کد باید دقیقاً 4 رقم باشد.',
        }
    )

    def __init__(self, *args, **kwargs):
        self.token = kwargs.pop('token', None)
        super().__init__(*args, **kwargs)

    def clean_code(self):
        code = self.cleaned_data['code']
        if not code.isdigit():
            raise forms.ValidationError('کد فقط باید شامل اعداد باشد.')

        # بررسی معتبر بودن توکن
        if not self.token:
            raise forms.ValidationError('توکن معتبر نیست!')

        try:
            otp = Otp.objects.get(code=code, token=self.token)
            if otp.created_at + timedelta(minutes=3) < now():
                otp.delete()
                raise forms.ValidationError('کد منقضی شده است. لطفاً دوباره درخواست دهید.')
        except Otp.DoesNotExist:
            raise forms.ValidationError('کد وارد شده معتبر نیست.')

        return code


class CompeletProfile(forms.Form):
    first_name = forms.CharField(
        max_length=50,
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'نام', 'class': 'form-control'})
    )
    last_name = forms.CharField(
        max_length=50,
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'نام خانوادگی', 'class': 'form-control'})
    )
    test = forms.TextInput(attrs={'class': 'form-control'})


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name']
