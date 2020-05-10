from django.shortcuts import render

# Create your views here.

def followView(request):
    fusername = request.POST.get('username')
    if request.user.is_authenticated:
        try:
            ent = Entrepeneur.objects.get(user.username = fusername)
        except: 
            return HttpResponse("User not found!")
        follow = Follow(
            actor = request.user
            target = ent
        )
        follow.save()
    return HttpResponseRedirect(reverse('feed:index'))

#input from template: project id
#in template, if entrepeneur viewing own project, show the post button, pass pid through context to feed/post
def postView(request): 
    pid = request.POST.get('pid')
    context ={}
    try:
        project = Project.objects.get(pk=pid)
        context['project'] = project
    except:
        return HttpResponse("Project not found")
    try: 
        funding_rounds = FundingRound.objects.filter(project=project)
        funding_round = funding_rounds.objects.latest()
        context['funding_round'] = funding_round
    if user.is_authenticated and request.user == project.creator.user: 
        if request.method == 'POST':
            #do this <-
        else:
            context['form'] = feed.forms.PostForm()
        return render(request, 'feed/post.html', context)
    else:
        return HttpResponse("Unauthorized action")

#tasks:
#1 - finish postView, check that it meets requirements of getstream
#2 - write funding round create view
