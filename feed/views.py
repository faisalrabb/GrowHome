from django.shortcuts import render
from stream_django.feed_manager import feed_manager
from account.models import User, Entrepreneur, Contributor
from projects.models import Project, FundingRound
from feed.forms import PostForm
from stream_django.enrich import Enrich
from django.db.models import Q
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

# Create your views here.

enricher = Enrich()


#template view
def index(request):
    context={}
    if not request.user.is_authenticated:
        return redirect(reverse('feed/about.html'))
    #
    feed = feed_manager.get_feed('timeline', request.user.id)
    activities = feed.get(limit=50)['results']
    enriched_activities = enricher.enrich_activities(activities)
    context['activities'] = enriched_activities
    #
    #notification_feed = feed_manager.get_notification_feed(request.user.id)
    #notifications = notification_feed.get(limit=50)['results']
    #notifications_enriched = enricher.enrich_activities(notifications)
    #context['notifications'] = notifications_enriched
    return render(request, 'feed/index.html', context)



#JSON view
@login_required
def followView(request, pid):
    try:
        proj = Project.objects.get(pk=pid)
    except: 
        return JsonResponse({'status': 'error', 'message': '404: Project not found'})
    follow = Follow.objects.filter(actor=request.user, target=proj)
    if follow is None:
        try: 
            follow = Follow(
                actor = request.user,
                target = proj
            )
            follow.save()
        except:
            return JsonResponse({'status': 'error', 'message': 'Error'})
    #else:
    #    try:
    #        follow.first().delete()
    #    except: 
    #        return JsonResponse({'status': 'error', 'message': 'Could not unfollow'})
    return JsonResponse({'status': 'success', 'message': 'ok'})

#JSON view
@login_required
def unfollowView(request, pid):
    try: 
        target = Project.objects.get(pk=pid)
        follow_instance = Follow.objects.get(actor=request.user, target=target)
    except:
        return JsonResponse({'status': 'error', 'message': 'could not fetch relevant follow instance'})
    follow_instance.delete()
    return JsonResponse({'status': 'success', 'message':'ok'})
    

#JSON view
@login_required
def postView(request, pid):
    context={}
    try:
        ent = Entrepreneur.objects.get(user=request.user)
        project = Project.objects.get(creator=ent, pk=pid)
    except:
        return JsonResponse({'status': 'error', 'message': 'Error submitting form'}) #raise Http404?
    if request.method=='POST':
        funding_rounds = FundingRound.objects.filter(project=project)
        if funding_rounds is not None:
            funding_round = funding_rounds.latest()
        else:
            funding_round = None
        form = feeds.forms.PostForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                post=Post(
                    project=project,
                    funding_round=funding_round,
                    title = form.cleaned_data['title'],
                    text = form.cleaned_data['text'],
                    pfile = form.cleaned_data['file'],
                    goal_accomplished= form.cleaned_data['goal_accomplished']
                )
                post.save()
                return JsonResponse({'status': 'success', 'message': 'success'})
            except:
                pass
    return JsonResponse({'status': 'error', 'message': 'error'})

#redirect view
@login_required
def deletePostView(request, post_identifier):
    try:
        actor = Entrepreneur.objects.get(user=request.user)
    except:
        return redirect(reverse('feed:index'))#non-entrepreneur redirect
    try:
        post = Post.objects.get(post_identifier=post_identifier)
    except:
        raise Http404 #post not found error
    if actor != post.project.creator:
        return redirect(reverse('feed:index'))#request didn't come from project creator
    post.delete() 
    return redirect(post.project)

#template view
@login_required
def editPostView(request, post_identifier):
    try:
        actor = Entrepreneur.objects.get(user=request.user)
    except:
        return HttpResponseRedirect(reverse('feed:index')) #Non-entrepreneur redirect
    try:
        post = Post.objects.get(post_identifier=post_identifier)
        funding_round = post.funding_round
    except:
        raise Http404 #Project not found error
    if actor != post.project.creator:
        return HttpResponseRedirect(reverse('feed:index')) #User is not project creator redirect
    if request.method=='POST':
        form = feed.forms.PostUpdateForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                post.title = form.cleaned_data['title']
                post.text = form.cleaned_data['text']
                post.goal_accomplished = form.cleaned_data['goal_accomplished']
                if form.cleaned_data['pfile'] is not None:
                    post.pfile=form.cleaned_data['pfile']
                post.save()
            except:
                form.add_error(None, "Error saving changes. Please try again.")
        else:
            form.add_error(None, 'One (or more) of the fields contain invalid values. Try again.')
        context['form'] = form
    else:
        goals= Goal.objects.filter(funding_round=funding_round, accomplished=False)
        context['form'] = feed.forms.PostForm(goals=goals, initial={'title': post.title, 'text': post.text, 'goal_accomplished' : post.goal_accomplished}) 
    return render(request, 'feed/edit.html', context)

#template view
#handles search and explore pages and functionality
def searchView(request):
    context={}
    form = feeds.forms.SearchForm(request.GET)
    if form.is_valid():
        query= form.cleaned_data['query']
        country= form.cleaned_data['country']
        looking_for = form.cleaned_data['looking_for']
        page_number = form.cleaned_data['page_number']
    if form.has_changed():
        page_number = 0
    else:
        query=None
        country=None
        looking_for = None
        page_number = 0
    if query is None and country is None:
        #explore selection
        matches = Project.objects.filter(seeking_funding=True).order_by('-featured', '-views')
    else:
        if query is None:
            query = ''
        matches = Project.objects.filter(Q(name__contains=query) | Q(problem__countains=query) | Q(solution__countains=query) | Q(info__countains=query)).order_by('-seeking_funding', '-views', '-likes')
        if country is not None:
            matches = matches.filter(country=country)
    if looking_for is not None:
        matches = matches.filter(looking_for__in=looking_for).distinct()
    paginator = Paginator(matches, 20)
    context['all-projects'] = matches
    try:
        page = paginator.page(page_number + 1)
    except PageNotAnInteger:
        page = paginator.page(1)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)
    context['projects'] = page
    context['form'] = feeds.forms.SearchForm(initial={'page_number': page.number, 'query': query,'country':country,'looking_for': looking_for})
    return render(request, 'feed/search.html', context)

#JSON view
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

#JSON view
@login_required
def unlikeView(request, content_type, content_id):
    if content_type == 'post':
        try:
            post = Post.objects.get(pk=content_id)
        except:
            return JsonResponse({'status': 'error', 'message': '404: Post not found'})
        like = Like.objects.filter(actor=request.user, target_post=post)
        if like is not None:
            p = like.first()
            p.delete()
    elif content_type == 'project':
        try:
            project = Project.objects.get(pk=content_id)
        except:
            return JsonResponse({'status': 'error', 'message': '404: Project not found'})
        like = Like.objects.filter(actor=request.user, target_project=project)
        if like is not None:
            p = like.first()
            p.delete()
    else:
        return JsonResponse({'status': 'error', 'message': 'invalid content type'})
    return JsonResponse({'status': 'success', 'message': 'ok'})

#JSON view    
#this view handles new comments (i.e. not replies to other comments). The comment text is taken from POST variable for integrity purposes (cannot post a comment on someone's behalf by getting them to click a link)
@login_required
def comment_on_post(request, pid):
    try:
        post = Post.objects.get(id=pid)
    except:
        return JsonResponse({'status': 'error', 'message': 'post not found'})
    if request.method == 'POST':
        form = feed.forms.CommentForm(request.POST)
        if form.is_valid():
            try:
                comment = Comment(actor=request.user, target=post, text=form.cleaned_data['text'])
                comment.save()
                return JsonResponse({'status': 'success', 'message':'success'})
            except:
                return JsonResponse({'status': 'error', 'message': 'error saving comment'})
        else:
            return JsonResponse({'status': 'error', 'message': 'invalid form'})
    else:
        return JsonResponse({'status': 'error'})
        
#JSON view
#same as above but for comments meant as replies to other comments
@login_required
def comment_on_comment(request, pid):
    try:
        comment = Comment.objects.get(id=pid)
    except:
        return JsonResponse({'status': 'error', 'message': 'comment not found'})
    if request.method == 'POST':
        form = feed.forms.CommentForm(request.POST)
        if form.is_valid():
            try:
                rcomment = CommentReply(actor=request.user, target=comment, text=form.cleaned_data['text'])
                rcomment.save()
                return JsonResponse({'status': 'success', 'message':'success'})
            except:
                return JsonResponse({'status': 'error', 'message': 'error saving comment'})
        else:
            return JsonResponse({'status': 'error', 'message': 'invalid form'})
    return JsonResponse({'status': 'error'})
        
#template view
def postDisplayView(request,post_identifier):
    context={}
    try:
        post = Post.objects.get(post_identifier=post_identifier)
    except:
        raise Http404
    context['post'] = post
    context['comments'] = Comment.objects.filter(post=post)
    return render(request, 'feed/post.html', context)

@login_required
def deleteCommentView(request, pid):
    comments = []
    com = Comment.objects.filter(id=pid)
    if com is not None:
        comments.append(com.first())
    comrep = CommentReply.objects.filter(id=pid)
    if comrep is not None:
        comments.append(comrep.first())
    for comment in comments:
        if comment.author == request.user:
            comment.delete()
            break
    return JsonResponse({'status' : 'success', 'message':'success'})






