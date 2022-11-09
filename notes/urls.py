from django.contrib import admin
from django.urls import path
from . import views

app_name = 'notes'
urlpatterns = [
    path('home/', views.PostListView.as_view(),
         name='home'),
    path('detail/<int:pk>', views.note_detail, #views.NoteDetailView.as_view()
         name='note-detail'),
    path('create/', views.note_created, # views.NoteCreateView.as_view()
         name='note-create'),
    path('<int:note_id>/share', views.note_share,
         name='share_note'),
    # path('<int:note_id>/create', views.post_comment,
    #      name='note_comment')
]