from django.shortcuts import render, redirect
from . import forms
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login, logout


# View function for registration with validation
def registration_view(request):
    form = forms.RegistrationForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect(reverse_lazy('user:login'))
    return render(request, 'user/registration.html', {'form': form})


# View function for logging in with form validation
def login_user_view(request):
    if request.method == 'POST':
        form = forms.LoginForm(request, request.POST)

        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            user = authenticate(email=username, password=password)
            if user is not None:
                login(request, user)
                return redirect(reverse_lazy('home:home'))

    else:
        form = forms.LoginForm()
    return render(request, 'user/login.html', {'form': form})


# View for logout and redirect to home page
def logout_user(request):
    logout(request)
    return redirect(reverse_lazy('home:home'))
