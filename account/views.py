from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db import IntegrityError
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from account.forms import SignInForm, ContributorSignup, EntrepreneurSignup
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm

# Create your views here.


def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('change_password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'account/change_password.html', {
        'form': form
    })


def entSignup(request):
    if request.user.is_authenticated:
        return redirect(reverse('feed:index')) 
    context={}
    if request.method == 'POST':
        form = account.forms.EntrepreneurSignup(request.POST, request.FILES)
        if form.is_valid():
            try:
                key = Key.objects.get(key=form.cleaned_data['invite_code'])
            except:
                form.add_error('invite_code', 'This invite code is not valid. If you believe this is a mistake, please contact us.')
                context['form'] = form
                return render(request, 'account/entrepreneursignup.html', context)
            if key.used:
                form.add_error(None,'This invite code has been used. If you believe this is a mistake, please contact us.')
                context['form'] = form
                return render(request, 'account/entrepreneursignup.html', context)
            try:
                user = User.objects.create_user(
                    first_name = form.cleaned_data['first_name'],
                    last_name = form.cleaned_data['last_name'],
                    username = form.cleaned_data['username'],
                    email = form.cleaned_data['email'],
                    password = form.cleaned_data['password']
                )
            except IntegrityError:
                form.add_error('username', 'This username is taken.')
                context['form'] = form
                return render(request, 'account/entrepreneurSignup.html', context)
            try:
                useraddress = form.cleaned_data['street_address'] + form.cleaned_data['city'] + form.cleaned_data['postcode']
                entrepreneur = Entrepreneur(
                    user = user,
                    country = form.cleaned_data['country'],
                    address = useraddress,
                    phone_number = form.cleaned_data['phone_number'],
                    profile_picture = form.cleaned_data['profile_picture'],
                    about = form.cleaned_data['about_you'],
                    bio = form.cleaned_data['bio'],
                    #identification = userid
                )
                entrepreneur.save()
                key.used = True
                key.save()
                return HttpResponseRedirect(reverse('account:login'))
            except:
                user.delete()
                form.add_error(None, 'Please make sure your files are in the correct format and try again.')
        context['form'] = form
    else:
        context['form'] = account.forms.EntrepreneurSignup()
    return render(request, 'account/entrepreneurSignup.html', context)

def contribSignup(request):
    if request.user.is_authenticated:
        return redirect(reverse('feed:index')) 
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
            except IntegrityError:
                form.add_error('username', 'Username is taken!')
                context['form'] = form
                return render(request, 'account/contributorSignup.html', context)
            try:
                contributor = Contributor(
                    user = user,
                    country = form.cleaned_data['country'],
                    bio = form.cleaned_data['bio'],
                    profile_picture = form.cleaned_data['profile_picture']
                )
                contributor.save()
                return HttpResponseRedirect(reverse('account:login'))
            except:
                form.add_error(None, "Please try again later.")
                user.delete()
        context['form'] = form
    else:
        context['form'] = account.forms.ContributorSignup()
    return render(request, 'account/contributorSignup.html', context)

def signin(request):
    if request.user.is_authenticated:
        return redirect(reverse('feed:index')) 
    context={}
    if request.method == 'POST':
        form = account.forms.SignInForm(request.POST)
        if form.is_valid():
            user = authenticate(request, username=form.cleaned_data['username'],password=form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                try: 
                    user_obj = Entrepreneur.objects.get(user = user)
                except:
                    user_obj = Contributor.objects.get(user=user)
                request.session['user_obj'] = user_obj
                return HttpResponseRedirect(reverse('feed:index'))
            else:
                form.add_error(None,'Invalid username or password')
        else:
            form.add_error(None,'Invalid input')
        context['form'] = form
    else:
        context['form'] = account.forms.SignInForm()
    return render(request, 'account/login.html', context)

@login_required
def signout(request):
    logout(request)
    return redirect(reverse('feed:index'))


def profileView(request): 
    context={}
    slug = request.GET.get('slug')
    if slug is None:
        if request.user.is_authenticated:
            user=request.user
            context['bio_update_form'] = account.forms.BioUpdateForm()
            context['contributions'] = Contribution.objects.filter(actor=request.user)
        else:
            return redirect(reverse('feed:index')) #if no slug is passed and user is not logged in
    else:
        try:
            user = User.objects.get(username=slug)
        except:
            return redirect(reverse('feed:index'))
    try:
        user_obj = Contributor.objects.get(user=user)
        context['type'] = "Contributor"
    except:
        user_obj = Entrepreneur.objects.get(user=user)
        projects = Project.objects.filter(creator=user_obj)
        posts = Post.objects.filter(actor__in=projects)
        context['posts'] = posts
        context['projects'] = projects
        context['type'] = "Entrepreneur"
    conext['country'] = user_obj.country
    #
    feed = feed_manager.get_feed('user', request.user.id)
    activities = feed.get()['results']
    enriched_activities = enricher.enrich_activities(activities)
    context['activities'] = enriched_activities
    #
    context['following'] = Follow.objects.filter(actor=user)
    return render(request, 'account/view.html', context)


def update_bio(request):
    if form.method == 'POST' and request.user.is_authenticated:
        form = account.forms.BioUpdateForm(request.POST)
        if form.is_valid():
            try:
                user_object = Contributor.objects.get(user=request.user)
            except:
                user_object = Entrepreneur.objects.get(user=request.user)
            user_object.bio = form.cleaned_data['bio']
            user_object.save()
            return JsonResponse({'status': 'success', 'message': 'success'})
    return JsonResponse({'status': 'error', 'message': 'unknown error'})
    
#not really meant for use at this stage
#@login_required
#def becomeEntrepreneurView(request):
#    try:
#        contributor = Contributor.objects.filter(user=request.user)
#    except:
#        return redirect(reverse(feed:index))
#    if form.method=='POST':
#        form = account.forms.EntrepeneurInfoForm(request.POST):
#        if form.is_valid():
#            try:
#                #might need to find less shit way of doing this
#                contributor.user = None
#                contributor.save()
#                entrepeneur = Entrepeneur(
#                    user=request.user,
#                    country=contributor.country,
#                    address = (form.cleaned_data['street_address'] +  ", " + form.cleaned_data['post_code'] + ", " + form.cleaned_data['city'])
#                    phone_number = form.cleaned_data['phone_number']
#                )
#                entrepeneur.save()
#                contributor.delete()
#            except:
#                contributor.user = request.user
#                contributor.save()
#                form.add_error(None,"An error occured. Please try again later")
#                context['form'] = form
#        else:
#            form.add_error(None, "Try again.")
#    else:
#        context['form'] = account.forms.EntrepeneurInfoForm()
#    return render(request, 'account/becomeEntrepeneur', context)



                
    


    
