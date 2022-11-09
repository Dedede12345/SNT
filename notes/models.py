from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import User

# Create your models here.
class DraftedManager(models.Manager):
    def get_query_set(self):
        return super(DraftedManager, self).get_query_set().\
            filter(status=Note.Status.DRAFT)

class PublishedManager(models.Manager):
    def get_query_set(self):
        return super(PublishedManager, self).get_query_set().\
            filter(status=Note.Status.PUBLISHED)

class Note(models.Model):

    draft = DraftedManager()
    published = PublishedManager()

    title = models.CharField(max_length=255)
    body = models.TextField(max_length=255)
    slug = models.SlugField()
    author = models.ForeignKey(
        User,
        related_name='notes',
        on_delete=models.CASCADE
        )

    class Status(models.TextChoices):
        DRAFT = 'DF', 'Drafted'
        PUBLISHED = 'PB', 'Published'

    status = models.CharField(
        max_length=2,
        default=Status.DRAFT,
        choices=Status.choices
    )

    publish = models.TimeField(default=timezone.now)
    created = models.TimeField(auto_now_add=True)
    updated = models.TimeField(auto_now=True)

    def __str__(self):
        return f"{self.title}_NOTE"

    def get_absolute_url(self):
        return reverse('notes:note-detail', kwargs={'pk': self.pk})

    class Meta:

        ordering = ['publish']
        # indexes = [
        #     models.Index(fields=['publish'])
        # ]

    objects = models.Manager()


class Comment(models.Model):

    author = models.ForeignKey(User, related_name='comments', on_delete=models.CASCADE)
    note = models.ForeignKey(Note, related_name='comments', on_delete=models.CASCADE)
    created = models.TimeField(auto_now_add=True)
    updated = models.TimeField(auto_now=True)
    body = models.TextField(max_length=255)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['created']
        indexes = [models.Index(fields=['created'])]

    def __str__(self):
        return f"{self.author.username}_comment_on_{self.note.title}"