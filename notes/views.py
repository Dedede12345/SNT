from django.shortcuts import render, redirect, reverse
from django.views import generic
from .models import Note, Comment
from .forms import NoteCreateForm, EmailNoteForm, CommentCreateForm
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from django.views.decorators.http import require_POST
import requests

# Create your views here.
def home(requset):
    notes = Note.published.all()
    return render(requset, 'notes/home.html', context={
        'notes': notes
    })

class PostListView(generic.ListView):
    model = Note
    template_name = 'notes/home.html'
    context_object_name = 'notes'
    paginate_by = 5

class NoteDetailView(generic.DetailView):
    model = Note
    context_object_name = 'note'
    extra_context = {
        'c_form': CommentCreateForm(),
    }

def note_detail(request, pk):
    note = Note.objects.get(id=pk)
    if request.method == 'POST':

        c_form = CommentCreateForm(request.POST)
        if c_form.is_valid():
            comment = c_form.save(commit=False)
            comment.note = note
            comment.author = request.user
            comment.save()
            return redirect(note.get_absolute_url())

    else:
        c_form = CommentCreateForm()

        return render(request, 'notes/note_detail.html', {
            'note': note,
            'comments': note.comments.filter(active=True),
            'c_form': c_form
        })
    

class NoteCreateView(generic.CreateView):
    model = Note
    fields = ['title', 'body']

    def form_valid(self, form):
        form.instance = self.request.user
        return super(NoteCreateView, self).form_valid(form)

def note_created(request):
    if request.method == 'POST':
        form = NoteCreateForm(data=request.POST)
        if form.is_valid():
            new_note = form.save(commit=False)
            new_note.author = request.user
            new_note.save()
            messages.success(request, "Note added successfully")
            return redirect(new_note.get_absolute_url())#redirect(f"/notes/detail/{new_note.pk}")
    else:
        form = NoteCreateForm(data=request.GET)
        return render(
            request,
            'notes/note_form.html',
            {
                'form': form
            }
        )

def note_share(request, note_id):
    note = get_object_or_404(Note, id=note_id) # status=Note.Status.PUBLISHED
    sent = False
    if request.method == 'POST':
        form = EmailNoteForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            #sending_mail
            url = request.build_absolute_uri(note.get_absolute_url())
            subject = f"{cd['name']} has shared a note with you"
            message = f"Read {note.title} at {url}\n\n" \
                      f"{cd['comments']}"
            send_mail(subject, message, 'gdenisov606@gmail.com', [cd['to']])
            sent = True
            messages.success(request, 'Mail sent successfully')
            return redirect('notes:home')

    else:
        form = EmailNoteForm()
        return render(request, 'notes/share.html', {'note': note, 'form': form, 'sent': sent})

@require_POST
def post_comment(request, note_id):
    note = get_object_or_404(Note, id=note_id)
    form = CommentCreateForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.note = note
        comment.save()
        messages.success(request, "Comment published")
        return redirect(note.get_absolute_url())