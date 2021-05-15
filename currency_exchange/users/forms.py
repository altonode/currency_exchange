from django.contrib.auth import forms as admin_forms
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django import forms

from currency_exchange.users.models import UserProfile
from currency_exchange.converter.models import Currency

User = get_user_model()


class UserChangeForm(admin_forms.UserChangeForm):

    class Meta(admin_forms.UserChangeForm.Meta):
        model = User


class UserCreationForm(admin_forms.UserCreationForm):

    class Meta(admin_forms.UserCreationForm.Meta):
        model = User

        error_messages = {
            "username": {"unique": _("This username has already been taken.")}
        }


class UserProfileForm(forms.ModelForm):
    query_set = Currency.objects.all()
    picture = forms.ImageField(required=False)
    preferred_currency = forms.ModelChoiceField(queryset=query_set, required=True)

    class Meta:

        model = UserProfile
        exclude = ('user',  'uuid', 'slug', )
