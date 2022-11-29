from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .forms import LoginForm, UserRegistrationForm, UserUpdateForm, ProfileUpdateForm
from django.contrib import messages
from django.views import generic
from .models import Profile
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Contacts


# Create your views here.
def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(
                request,
                username=cd['username'],
                password=cd['password']
            )
            if user:
                if user.is_active:
                    login(request, user)
                    return redirect('notes:home')
                else:
                    return HttpResponse('Disabled account')
            else:
                messages.warning(request, 'Failed to login')
                return render(request, 'account/login.html',
                              context={'form': form})
    else:
        form = LoginForm()
        return render(
            request,
            'account/login.html',
            context={
                'form': form
            }
        )


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Successfully registered")
            return redirect('login')
        else:
            messages.warning(request, 'Error has occurred')
            return render(request, 'account/register.html', {
                'form': form
            })
    else:
        form = UserRegistrationForm()
        return render(request, 'account/register.html', context={
            'form': form
        })


@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, files=request.FILES,
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Profile successfully updated')
            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
        return render(request, 'account/profile.html', context={
            'u_form': u_form, 'p_form': p_form
        })


class ProfileDetailView(generic.DetailView):
    model = Profile


@login_required
def profile_detail_view(request, id):
    if request.method == 'GET':
        profile = Profile.objects.get(id=id)
        return render(request, 'account/profile-detail.html',
                      {
                          'profile': profile,
                      })


@login_required
def user_list(request):
    users = User.objects.filter(is_active=True)
    return render(request, 'account/user_list.html',
                  {
                      'users': users
                  })
@login_required
def user_detail(request, username):
    user = get_object_or_404(User, id=username, is_active=True)
    return render(request, 'account/user_detail.html',
                  {
                      'users': user
                  })


@require_POST
@login_required
def user_follow(request):
    user_id = request.POST.get('id')
    action = request.POST.get('action')
    if user_id and action:
        try:
            user = User.objects.get(id=user_id)
            if action == 'follow':
                Contacts.objects.get_or_create(
                    user_from=request.user,
                    user_to=user
                )
                # create_action(request.user, 'is following', user)
            else:
                Contacts.objects.filter(user_from=request.user,
                                       user_to=user).delete()
            return JsonResponse({'status': 'ok'})
        except User.DoesNotExist:
            return JsonResponse({'status': 'error'})
        finally:
            print('Resulted in any kind of shit')
    print(f'Resulted in any kind of shit')
    return JsonResponse({'status': "error"})