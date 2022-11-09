from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .forms import LoginForm, UserRegistrationForm, UserUpdateForm, ProfileUpdateForm
from django.contrib import messages

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