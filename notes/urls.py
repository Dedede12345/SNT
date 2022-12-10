from django.contrib import admin
from django.urls import path
from . import views

app_name = 'notes'
urlpatterns = [
    path('home/', views.home,
         name='home'),
    path('detail/<int:pk>', views.note_detail, #views.NoteDetailView.as_view()
         name='note-detail'),
    path('create/', views.note_created, # views.NoteCreateView.as_view()
         name='note-create'),
    path('<int:note_id>/share', views.note_share,
         name='share_note'),
    path('like/', views.note_like,
         name='like'),
    path('testing/', views.testing, name='testing'),
    path('search/', views.note_search,
         name='note_search')
    # path('<int:note_id>/create', views.post_comment,
    #      name='note_comment')
]