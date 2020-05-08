from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.db import IntegrityError
from django.urls import reverse
from django.contrib.auth.decorators import login_required
import account.forms
import account.models


# Create your views here.

def entSignup(request): 
    context={}
    if request.method == 'POST':
        form = account.forms.EntrepeneurSignup(request.POST)
        if form.is_valid():
            try:
                user = User.objects.create_user(
                    first_name = form.cleaned_data['first_name'],
                    last_name = form.cleaned_data['last_name'],
                    username = form.cleaned_data['username'],
                    email = form.cleaned_data['email'],
                    password = form.cleaned_data['password']
                )
                useraddress = form.cleaned_data['street_address'] + form.cleaned_data['city'] + form.cleaned_data['postcode']
                userid = Identification( 
                    file = form.cleaned_data['identification']
                )
                userid.save()
                entrepeneur = Entrepeneur(
                    user = user
                    country = form.cleaned_data['country']
                    address = useraddress
                    phone_number = form.cleaned_data['phone_number']
                    identification = userid
                )
                entrepeneur.save()
                return HttpResponseRedirect(reverse('account:login'))
            except IntegrityError:
                form.add_error('username', 'Username is taken!')
        context['form'] = form
    else:
        context['form'] = account.forms.EntrepeneurSignup()
    return render(request, 'account/entrepeneurSignup.html', context)

def contribSignup(request):
    context={}
    if request.method == 'POST':
        form = account.forms.ContributorSignup(request.POST)
        if form.is_valid():
            try:
                user = User.objects.create_user(
                    first_name = form.cleaned_data['first_name'],
                    last_name = form.cleaned_data['last_name'],
                    username = form.cleaned_data['username'],
                    email = form.cleaned_data['email'],
                    password = form.cleaned_data['password']
                )
                contributor = Contributor(
                    user = user,
                    country = form.cleaned_data['country'],
                )
                contributor.save()
                return HttpResponseRedirect(reverse('account:login'))
            except IntegrityError:
                form.add_error('username', 'Username is taken!')
        context['form'] = form
    else:
        context['form'] = account.forms.ContributorSignup()
    return render(request, 'account/contributorSignup.html', context)

def signin(request):
    context={}
    if request.method == 'POST':
        form = account.forms.SignInForm(request.POST)
        if form.is_valid():
            user = authenticate(request, username=form.cleaned_data['username'],password=form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse('feed:index'))
            else:
                form.add_error(None,'Invalid username or password')
        else:
            form.add_error(None,'Invalid input')
        context['form'] = form
    else:
        context[form] = account.forms.SignInForm()
    return render(request, 'account/login.html', context)

@login_required
def signout(request):
    logout(request)
    return HttpResponseRedirect(reverse('feed:index'))
             


    
