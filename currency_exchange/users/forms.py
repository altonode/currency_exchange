from django.contrib.auth import forms as admin_forms
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django import forms

from allauth.account.forms import SignupForm

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

        model = User
        fields = ('username', 'preferred_currency', 'picture', )


# UserSignupForm inherits from django-allauth's SignupForm
class UserSignupForm(SignupForm):
    # Query for all supported currencies
    query_set = Currency.objects.all()
    preferred_currency = forms.ModelChoiceField(queryset=query_set, required=True)
    picture = forms.ImageField(required=False)

    # Put in custom signup logic
    def custom_signup(self, request, user):

        # Set the user's type from the form response
        user.preferred_currency = self.cleaned_data["preferred_currency"]
        # Set the user's type from the form response
        user.picture = self.cleaned_data["picture"]

        # Save the user's picture and currency to their database record
        user.save()
