from django.contrib import admin
from .models import Note, Comment

# Register your models here.
@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ['title', 'body', 'author', 'publish']
    list_filter = ['author', 'publish']
    search_fields = ['author', 'title']
    prepopulated_fields =  {'slug': ('title', )}


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['author', 'note']
    list_filter = ['author', 'active', 'note']
    search_fields = ['author']
