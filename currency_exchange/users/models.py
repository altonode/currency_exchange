import uuid as uuid_lib

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.template.defaultfilters import slugify


class User(AbstractUser):
    """Default user for Currency Exchange Project."""

    #: First and last name do not cover name patterns around the globe
    name = models.CharField(_("Name of User"), blank=True, max_length=255)
    first_name = None  # type: ignore
    last_name = None  # type: ignore

    def get_absolute_url(self):
        """Get url for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"username": self.username})

class UserProfile(models.Model):
    # Links UserProfile to a User model instance.
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE,
    )

    # Additional User attributes to include.
    picture = models.ImageField(upload_to='profile_images', blank=True)

    # user record unique identifier
    uuid = models.UUIDField(
        db_index=True,
        default=uuid_lib.uuid4,
        editable=False)
    # web api url slug
    slug = models.SlugField(unique=True, blank = True)

    # update record
    def save(self, *args, **kwargs):
        self.slug = slugify(self.uuid)
        super(UserProfile, self).save(*args, **kwargs)

    # Return the user's name
    def __str__(self):
        return self.user.username
