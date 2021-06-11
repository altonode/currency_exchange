import uuid as uuid_lib

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.template.defaultfilters import slugify

from currency_exchange.converter.models import Currency


class User(AbstractUser):
    """Default user for Currency Exchange Project."""
    #: Username
    name = models.CharField(_("Name of User"), blank=True, max_length=255)
    first_name = None  # type: ignore
    last_name = None  # type: ignore
    picture = models.ImageField(upload_to='user_images', blank=True, null=True)
    preferred_currency = models.ForeignKey(Currency, blank=True, null=True,
                                           on_delete=models.CASCADE)
    # user record url unique identifier
    uuid = models.UUIDField(
        db_index=True,
        default=uuid_lib.uuid4,
        editable=False)

    def get_absolute_url(self):
        """
        Get url for user's detail view.
        """
        return reverse("users:detail", kwargs={"username": self.username})
