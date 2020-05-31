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



def index(request):
    if !request.user.is_authenticated:
        return redirect(reverse('about:index'))
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
def followView(request, pid):
    #fusername = kwargs['username']
    try:
        proj = Project.objects.get(pk=pid)
    except: 
        return JsonResponse({'status': 'error', 'message': '404: User not found'})
    if Follow.objects.filter(actor=request.user, target=ent) is None:
        follow = Follow(
            actor = request.user
            target = ent
        )
        follow.save()
    return JsonResponse({'status': 'success', 'message': 'ok'})

@login_required
def unfollowView(request, pid):
    try: 
        target = Project.objects.get(pk=pid)
        follow_instance = Follow.objects.get(actor=request.user, target=target)
    except:
        return JsonResponse({'status': 'error', 'message': 'could not fetch relevant follow instance'})
    follow_instance.delete()
    return JsonResponse({'status': 'success', 'message':'ok'})
    

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
        return HttpResponse("Project initialization error. Please try later.") #should never happen
    if user.is_authenticated and request.user == project.creator.user: 
        if request.method == 'POST':
            form = feed.forms.postView(request.POST, request.FILES)
            try:
                post = Post(
                project = project,
                poster = request.user
                funding_round = funding_round,
                title = form.cleaned_data['title'],
                text = form.cleaned_data['text'],
                pfile = form.cleaned_data['file'],
                goal_accomplished= form.cleaned_data['goal_accomplished']
                )
                post.save()
            except:
                form.add_error(None, "Form submission error. Try again. If this problem persists, contact support.") #form error 
        else:
            goals= Goal.objects.filter(funding_round=funding_round, accomplished=False)
            context['form'] = feed.forms.PostForm(goals=goals)
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
                post_edit = Post(
                    id = post.pk,
                    title = form.cleaned_data['title'],
                    text = form.cleaned_data['text'],
                    pfile = form.cleaned_data['pfile'],
                    goal_accomplished = form.cleaned_data['goal_accomplished']
                    )
                if form.cleaned_data['pfile'] is not None:
                    post_edit.pfile=form.cleaned_data['pfile']
                post_edit.save()
            except:
                form.add_error(None, "Unknown Error occured. Please try again later or contact support.")
        else:
            form.add_error(None, 'Try again.')
        context['form'] = form
    else:
        goals= Goal.objects.filter(funding_round=funding_round, accomplished=False)
        context['form'] = feed.forms.PostUpdateForm(goals=goals, initial={'title': post.title, 'text': post.text}) #<- fill
    return render(request, 'feed/edit.html', context)



#accepts three optional GET parameters (query, country, and page_number), if query and country are None, the "explore" selection is returned
def searchView(request)
    query = request.GET.get('q', None)
    country = request.GET.get('country_name', None)
    page_number = request.GET.get('page_number', None)
    if country_name is not None:
        try:
            country = Country.objects.get(name=country_name)
        except:
            country = None

    if query is None and country is None:
        #explore selection
        matches = Project.objects.filter(seeking_funding=True).order_by('-views', '-featured')
    if request.method == 'POST':
        #Form submitted (i.e. actual search query)
        form = feed.forms.SearchForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data['query']
            country = form.cleaned_data['country']
    if query is None:
        query = ''
    matches = Project.objects.filter(Q(name__contains=query) | Q(problem__countains=query) | Q(solution__countains=query) | Q(info__countains=query)).order_by('-seeking_funding', '-views', '-likes')
    if country is not None:
        matches = matches.filter(country=country)
    
    paginator = Paginator(matches, 20)
    #context['all-projects'] = matches
    try:
        context['projects'] = paginator.page(page_number)
    except PageNotAnInteger:
        context['projects'] = paginator.page(1)
    except EmptyPage:
        context['projects'] = paginator.page(paginator.num_pages)
    return render(request, 'feed/search.html', context)

@login_required
def likeView(request, content_type, content_id):
    if content_type == 'post':
        try:
            post = Post.objects.get(pk=content_id)
        except:
            return JsonResponse({'status': 'error', 'message': '404: Post not found'})
        if Like.objects.filter(actor=request.user, target_post=post) is None:
            like = Like(actor = request.user, target_post = post)
            like.save()
    elif content_type == 'project':
        try:
            project = Project.objects.get(pk=content_id)
        except:
            return JsonResponse({'status': 'error', 'message': '404: Project not found'})
        if Like.objects.filter(actor=request.user, target_project=project) is None:
            like = Like(actor = request.user, target_project=project)
            like.save()
    else:
        return JsonResponse({'status': 'error', 'message': 'invalid content type'})
    return JsonResponse({'status': 'success', 'message': 'ok'})

@login_required
def unlikeView(request, content_type, content_id):
    if content_type == 'post':
        try:
            post = Post.objects.get(pk=content_id)
        except:
            return JsonResponse({'status': 'error', 'message': '404: Post not found'})
        like = Like.objects.filter(actor=request.user, target_post=post):
        if like is not None:
            p = like.first()
            p.delete()
    elif content_type == 'project':
        try:
            project = Project.objects.get(pk=content_id)
        except:
            return JsonResponse({'status': 'error', 'message': '404: Project not found'})
        like = Like.objects.filter(actor=request.user, target_project=project):
        if like is not None:
            p = like.first()
            p.delete()
    else:
        return JsonResponse({'status': 'error', 'message': 'invalid content type'})
    return JsonResponse({'status': 'success', 'message': 'ok'})
    

    

