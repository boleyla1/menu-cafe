from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User,Otp
from .forms import UserChangeForm, UserCreationForm


class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ["phone", "is_admin"]
    list_filter = ["is_admin"]
    fieldsets = [
        (None, {"fields": ["phone", "password"]}),
        ("Personal info", {"fields": ["first_name", "last_name"]}),
        ("Permissions", {"fields": ["is_admin"]}),
    ]
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = [
        (
            None,
            {
                "classes": ["wide"],
                "fields": ["phone", "first_name",'last_name', "password1", "password2"],
            },
        ),
    ]
    search_fields = ["phone"]
    ordering = ["phone"]
    filter_horizontal = []



@admin.register(Otp)
class OtpAdmin(admin.ModelAdmin):
    list_display = ('phone', 'code', 'token', 'created_at', 'is_valid')
    list_filter = ('created_at',)
    search_fields = ('phone', 'token')

    def is_valid(self, obj):
        from django.utils.timezone import now
        from datetime import timedelta
        return now() - obj.created_at <= timedelta(minutes=3)

    is_valid.boolean = True
    is_valid.short_description = "کد معتبر است؟"


# Now register the new UserAdmin...
admin.site.register(User, UserAdmin)


# ... and, since we're not using Django's built-in permissions,
# unregister the Group model from admin.
admin.site.unregister(Group)
