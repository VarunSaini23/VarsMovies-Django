from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect

from accounts.forms import SignUpForm


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'accounts/signup.html', {'form': form})


def auth_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        raw_password = request.POST.get('password')
        user = authenticate(username=username, password=raw_password)
        if(request.user.is_authenticated):
            login(request, user)
            return redirect('user_home_page', request.user.username)
        else:
            return redirect('signup')
    else:
        form = SignUpForm()
    return render(request, 'accounts/login.html', {'form': form})
