from django import forms
from .models import Category, Product, CafeSettings


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'image']


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'ingredients', 'price', 'category', 'image']


class CafeSettingsForm(forms.ModelForm):
    class Meta:
        model = CafeSettings
        fields = ['name', 'address', 'phone_number', 'instagram_handle']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'نام کافه', 'dir': 'rtl'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'آدرس کامل', 'dir': 'rtl'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'شماره تماس', 'dir': 'rtl'}),
            'instagram_handle': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'آیدی اینستاگرام', 'dir': 'rtl'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].label = "نام کافه"
        self.fields['address'].label = "آدرس کامل"
        self.fields['phone_number'].label = "شماره تماس"
        self.fields['instagram_handle'].label = "آیدی اینستاگرام"
        # افزودن ولیدیشن اضافی
        self.fields['phone_number'].validators.append(self.validate_phone_number)

    def validate_phone_number(self, value):
        if not value.isdigit():
            raise forms.ValidationError("شماره تماس باید فقط شامل اعداد باشد.")
