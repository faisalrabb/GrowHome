from django.shortcuts import render
from stream_django.feed_manager import feed_manager
from account.models import User, Entrepeneur, Contributor
from projects.models import Project, FundingRound
from feed.forms import PostForm, PostUpdateForm
from stream_django.enrich import Enrich
from django.db.models import Q
from django.core.paginator import Paginator
# Create your views here.

enricher = Enrich()


@login_required
def index(request):
    feeds = feed_manager.get_news_feeds(request.user.id)
    activities = feeds.get('timeline').get()['results']
    enriched_activities = enricher.enrich_activities(activities)
    notification_feed = client.feed('notification', current_user.id)
    notifications = notification_feed.get()['results']
    notifications_enriches = enricher.enrich_activities(notifications)
    context['activities'] = enriched_activities
    context['login_user'] = request.user
    context['notifications'] = notifications_enriched
    context['search_form'] = feed.forms.SearchForm()
    return render(request, 'feed/index.html', context)




@login_required
def followView(request, fusername):
    #fusername = kwargs['username']
    try:
        ent = Entrepeneur.objects.get(user.username = fusername)
    except: 
        return HttpResponse("User not found!")
    if Follow.objects.filter(actor=request.user, target=ent) is None:
        follow = Follow(
            actor = request.user
            target = ent
        )
        follow.save()
    return HttpResponseRedirect(reverse('feed:index'))

@login_required
def unfollowView(request, fusername):
    try: 
        target = Entrepeneur.objects.get(username=fusername)
        follow_instance = Follow.objects.get(actor=request.user, target=target)
    except:
        return HttpResponseRedirect(reverse('feed:index')) # failure redirect, no error message
    follow_instance.delete()
    

#in template, if entrepeneur viewing own project, show the post button, pass pid through context to feed/post
@login_required
def postView(request, pid): 
    #pid = kwargs['pid']
    context ={}
    try:
        project = Project.objects.get(pk=pid) 
        context['project'] = project
    except:
        return HttpResponse("Project not found") #project not found error
    try: 
        funding_rounds = FundingRound.objects.filter(project=project)
        funding_round = funding_rounds.objects.latest()
        context['funding_round'] = funding_round
        context['goals'] = [funding_round.goal_1, funding_round.goal_2, funding_round.goal_3]
    except:
        return HttpResponse("Project initialization error. Please contact support.") #should never happen
    if user.is_authenticated and request.user == project.creator.user: 
        if request.method == 'POST':
            form = feed.forms.postView(request.POST, request.FILES)
            try:
                post = Post(
                project = project,
                funding_round = funding_round,
                title = form.cleaned_data['title'],
                text = form.cleaned_data['text'],
                pfile = form.cleaned_data['file'],
                )
                if form.cleaned_data['goal_accomplished'] is None:
                    post.goal_accomplished = True
                    if goal_accomplished==1:
                        funding_round.goal_1_finished = True
                        post.goal_text = funding_round.goal_1
                    elif goal_accomplished == 2:
                        funding_round.goal_1_finished = True
                        post.goal_text = funding_round.goal_2
                    elif goal_accomplished == 3:
                        funding_round.goal_1_finished = True
                        post.goal_text = funding_round.goal_3
                    funding_round.save()
                post.save()
                goal_accomplished = form.cleaned_data['goal_accomplished']  
            except:
                form.add_error(None, "Form submission error. Try again. If this problem persists, contact support.") #form error 
        else:
            context['form'] = feed.forms.PostForm()
        return render(request, 'feed/post.html', context) #GET-request redirect
    else:
        return HttpResponse("Unauthorized action") #non-creator error
    return redirect(project) #success redirect

@login_required
def deletePostView(request, post_identifier):
    try:
        actor = Entrepeneur.objects.get(user=request.user)
    except:
        return HttpResponseRedirect(reverse('feed:index'))#non-entrepeneur redirect
    try:
        post = Post.objects.get(post_identifier=post_identifier)
    except:
        return HttpResponse("Post not found") #post not found error
    if actor != post.project.creator:
        return HttpResponseRedirect(reverse('feed:index'))#request didn't come from project creator
    post.delete() 

@login_required
def editPostView(request, post_identifier):
    try:
        actor = Entrepeneur.objects.get(user=request.user)
    except:
        return HttpResponseRedirect(reverse('feed:index')) #Non-entrepeneur redirect
    try:
        post = Post.objects.get(post_identifier=post_identifier)
        funding_round = post.funding_round
    except:
        return HttpResponse("Project not found") #Project not found error
    if actor != post.project.creator:
        return HttpResponseRedirect(reverse('feed:index')) #User is not project creator redirect
    if request.method=='POST':
        form = feed.forms.PostUpdateForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                if form.cleaned_data['pfile'] is not None:
                    post_edit = Post(
                        id = post.pk,
                       title = form.cleaned_data['title'],
                       text = form.cleaned_data['text'],
                       pfile = form.cleaned_data['pfile'],
                    )
                else:
                    post_edit = Post(
                        id = post.pk,
                        title = form.cleaned_data['title'],
                        text = form.cleaned_data['text']
                    )
                if form.cleaned_data['goal_accomplished'] is None:
                    post.goal_accomplished = True
                    if goal_accomplished==1:
                        funding_round.goal_1_finished = True
                        post_edit.goal_text = funding_round.goal_1
                    elif goal_accomplished == 2:
                        funding_round.goal_1_finished = True
                        post_edit.goal_text = funding_round.goal_2
                    elif goal_accomplished == 3:
                        funding_round.goal_1_finished = True
                        post_edit.goal_text = funding_round.goal_3
                    funding_round.save()
                post_edit.save()
            except:
                form.add_error(None, "Unknown Error occured. Please try again later or contact support.")
        else:
            form.add_error(None, 'Try again.')
        context['form'] = form
    else:
        context['form'] = feed.forms.PostUpdateForm(initial={'title': post.title, 'text': post.text}) #<- fill
    return render(request, 'feed/edit.html', context)

#build discover on top of search view
def searchView(request, page_number)
    if request.method == 'GET':
        #explore view
        matches = Project.objects.filter(seeking_funding=True).order_by('-views')
    if request.method == 'POST':
        #Form submitted (i.e. actual search query)
        form = feed.forms.SearchForm(request.POST)
        if form.is_valid():
            term = form.cleaned_data['term']
            country = form.cleaned_data['country']
            matches = Project.objects.filter(Q(name__contains=term) | Q(problem__countains=term) | Q(solution__countains=term) | Q(info__countains=term)).order_by('-seeking_funding', '-views')
            if country is not None:
                matches = matches.filter(country=country)
    paginator_object = Paginator(matches, 20)
    #context['all-projects'] = matches
    context['paginator'] = paginator_object.get_page(page_number)
    return render(request, 'feed/search.html', context)



