from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from django.contrib.auth import get_user_model
class Profile(models.Model):

    class Status(models.TextChoices):
        OWN = 'OW', 'Own'
        FORWARDED = 'FWD', 'Forwarded'

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    # description = models.TextField(on_delete=models.CASCADE)
    image = models.ImageField(default='media/default.jpg',
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

class Contacts(models.Model):

    user_from = models.ForeignKey(
        'auth.User',
        related_name='rel_from_set',
        on_delete=models.CASCADE
    )

    user_to = models.ForeignKey(
        'auth.User',
        related_name='rel_to_set',
        on_delete=models.CASCADE
    )

    created = models.TimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['created'])
        ]

        ordering = ['-created']

    def __str__(self):
        return f"{self.user_from}_follows_{self.user_to}"

user_model = get_user_model()
user_model.add_to_class('following',
                        models.ManyToManyField(
                            'self',
                            through=Contacts,
                            related_name='followers',
                            symmetrical=False
                        ))