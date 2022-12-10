from django.shortcuts import render, redirect, reverse
from django.views import generic
from .models import Note, Comment
from .forms import NoteCreateForm, EmailNoteForm, SearchForm, CommentCreateForm
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from actions.utils import create_action
from actions.models import Action
import requests
from django.core.paginator import Paginator
from django.contrib.postgres.search import SearchVector

# Create your views here.
def home(request):
    actions = Action.objects.all()
    following_ids = request.user.following.values_list('id', flat=True)


    if following_ids:
        actions = actions.filter(user_id__in=following_ids)
    actions = actions[:5]
    notes = Note.objects.all()
    paginator = Paginator(notes, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'notes/home.html', context={
        'notes': notes,
        'actions': actions,
        'page_obj': page_obj,
        'section': 'actions'
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
            create_action(request.user, 'commented note', comment)
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
            create_action(request.user, 'created note', new_note)
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
            message = messages.error(request, "Somethig went wrong")
            return render(request, 'notes/share.html', {'note': note, 'form': form, 'sent': sent})

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
        # create_action(request.user, 'created note', new_note)
        messages.success(request, "Comment published")
        return redirect(note.get_absolute_url())


@require_POST
@login_required
def note_like(request):
    note_id = request.POST.get('id')
    action = request.POST.get('action')
    print(note_id, action)
    if note_id and action:
        try:
            note = Note.objects.get(id=note_id)
            if action == 'like':
                note.users_like.add(request.user)
                create_action(request.user, 'likes', note)

            else:
                note.users_like.remove(request.user)
            return JsonResponse({'status': 'ok'})
        except Note.DoesNotExist:
            pass

    return JsonResponse({'status': 'error'})

def testing(request):
    actions = Action.objects.all()
    return render(request, 'notes/testing.html', context={
        'actions': actions
    })

def note_search(request):
    form = SearchForm()
    query = None
    results = []

    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            results = Note.published.annotate(
                search=SearchVector('title', 'body')
            ).filter(search=query)

    return render(request, 'notes/search.html',
                      {
                          'form': form,
                          'query': query,
                          'results': results
                      })