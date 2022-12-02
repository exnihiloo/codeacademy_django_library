from django.contrib.auth import get_user_model
from django.db import models
from PIL import Image
from django.utils.translation import gettext_lazy as _


class Profile(models.Model):
    user = models.OneToOneField(
        get_user_model(), 
        verbose_name=_("user"), 
        on_delete=models.CASCADE,
        related_name="profile",
    )
    photo = models.ImageField(_("photo"), upload_to='user_profile/photos', null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.user} profile"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.photo:
            photo = Image.open(self.photo.path)
            if photo.width > 500 or photo.height > 500:
                output_size = (500, 500)
                photo.thumbnail(output_size)
                photo.save(self.photo.path)