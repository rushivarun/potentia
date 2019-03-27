from django.shortcuts import render, redirect
from loginSignup.forms import UserForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .forms import AddSignupForm


def index(request):
    return render(request, 'loginSignup/index.html')


@login_required
def special(request):
    return HttpResponse("You are logged in !")


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))


def register(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        add_form = AddSignupForm(data = request.POST)
        if user_form.is_valid() and add_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            adf = add_form.save(commit=False)
            adf.user = user
            adf.save()
            registered = True
            login(request, user)
            return redirect('index')
        else:
            print(user_form.errors)
    else:
        user_form = UserForm()
        add_form = AddSignupForm()
    return render(request, 'loginSignup/registration.html',
                  {'user_form': user_form, 'add_form': add_form,
                           'registered': registered})


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse("Your account was inactive.")
        else:
            print("Someone tried to login and failed.")
            print("They used username: {} and password: {}".format(
                username, password))
            return HttpResponse("Invalid login details given")
    else:
        return render(request, 'loginSignup/login.html', {})
