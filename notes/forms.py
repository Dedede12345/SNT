from .models import Note, Comment
from django.core.files.base import ContentFile
from django.utils.text import slugify
from django import forms
import requests

class NoteCreateForm(forms.ModelForm):

    class Meta:

        model = Note
        fields = ['title', 'body']
        widgets = {
            'url': forms.HiddenInput
        }

    def save(self, commit=True, force_insert=False):

        note = super(NoteCreateForm, self).save(commit=False)

        if commit:
            note.save()
        return note

class EmailNoteForm(forms.Form):
    name = forms.CharField(max_length=255)
    # email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False,
                               widget=forms.Textarea)

class CommentCreateForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ['body']


class SearchForm(forms.Form):
    query = forms.CharField()
