from django.db import models
from django.contrib.auth.models import User
from PIL import Image
class Profile(models.Model):

    class Status(models.TextChoices):
        OWN = 'OW', 'Own'
        FORWARDED = 'FWD', 'Forwarded'

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg',
                              upload_to='profile_pics')
    # type = models.CharField(choices=Status.choices)


    def save(
        self, *args, **kwargs
    ):
        super(Profile, self).save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)

