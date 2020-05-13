from django.shortcuts import render
from feed.models import Post
from projects.forms import ProjectForm, FundingRoundForm
from projects.models import FundingRound, Project
from account.models import User, Entrepeneur
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def newProject (request):
    context={}
    try:
        entrepeneurInstance = Entrepeneur.objects.filter(user = request.user)
    except:
        return HttpResponseRedirect(reverse(feed:index)) #non-entrepeneur redirect
    if request.method == 'POST':
        form = projects.forms.ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                this_project = Project(
                    creator = entrepeneurInstance,
                    name = form.cleaned_data['name'],
                    problem = form.cleaned_data['problem'],
                    solution = form.cleaned_data['solution'],
                    info = form.cleaned_data['info'],
                    country = entrepeneurInstance.country,
                    city = form.cleaned_data['city'],
                    intro_video = form.cleaned_data['video'],
                    photo = form.cleaned_data['photo']
                )
                this_project.save()
                fundinground = FundingRound(
                    project = this_project,
                    funding_goal = form.cleaned_data['funding_goal'],
                    goal_1 = form.cleaned_data['goal_1'],
                    goal_2 = form.cleaned_data['goal_2'],
                    goal_3 = form.cleaned_data['goal_3'],
                    info = form.cleaned_data['info'],
                    video = form.cleaned_data['video'],
                    note = form.cleaned_data['note']
                )
                fundinground.save()
                return redirect(this_project) #success redirect
            except IntegrityError:
                form.add_error('project', 'Project name already exists.')
        context['form'] = form
    else:
        context['form'] = projects.forms.ProjectForm()
    return render(request,'projects/new.html', context) #try again redirect


#funding round: 1. check active project, 2. check last funding round status (closed, 3 goals accomplished)
@login_required
def newFundingRound(request, pid):
    context={}
    try:
        entrepeneur = Entrepeneur.objects.get(user=request.user)
        project = Project.objects.get(pk=pid)
        fundingrounds = FundingRound.objects.filter(project=project)
        if fundingrounds is None:
            return HttpsResponse("Previous funding rounds not found") #Error in project initialization. In theory this line should never run
        else:
            fundinground = fundingrounds.latest()
        if project.creator != entrepeneur:
            return HttpResponse("Unauthorized") #project not created by user - shouldn't trigger unless malicious attempt
    except: 
        return HttpResponseRedirect(reverse('feed:index')) #non-entrepeneur redirect
    if request.method == 'POST':
        form = projects.forms.FundingRoundForm(request.POST, request.FILES)
        if not (fundinground.goal_1_finished and fundinground.goal_2_finished and fundinground.goal_3_finished):
            form.add_error(None, "Your previous funding round has unaccomplished goals. Mark these as completed in order to start a new funding round. If you believe this is an error, please contact support.")
        else if form.is_valid():
            try:
                frnumber = fundinground.round_number + 1
                fundinground = FundingRound(
                    project = project,
                    funding_goal = form.cleaned_data['funding_goal'],
                    round_number = frnumber,
                    goal_1 = form.cleaned_data['goal_1'],
                    goal_2 = form.cleaned_data['goal_2'],
                    goal_3 = form.cleaned_data['goal_3'],
                    info = form.cleaned_data['info'],
                    video = form.cleaned_data['video'],
                    note = form.cleaned_data['note'],
                )
                fundinground.save()
                return redirect(project) #success redirect 
            except IntegrityError:
                form.add_error(None, 'Error saving funding round. Please try again later. If this problem persists, contact support')
    else:
        context['form'] = projects.forms.FundingRoundForm()
        context['project'] = project
    return render(request, '/projects/newfundinground.html', context) #retry redirect

@login_required
def editProject(request, pid):
    try:
        project= Project.objects.get(pk=pid)
    except:
        return HttpResponse("Project not found") #project not found error
    try:
        creator = Entrepeneur.objects.get(user=request.user)
    except:
        return HttpResponseRedirect(reverse('feed:index')) #non-entrepeneur redirect
    if creator != project.creator:
        return HttpResponseRedirect(reverse('feed:index')) # redirect for when someone tries to edit a project that's not theirs, shouldn't happen unless malicious attempt
    context={}
    if form.method == 'POST':
        form = projects.forms.ProjectForm(request.POST, request.FILES)
        if form.is_valid() and form.has_changed():
            try:
                project_edit = Project(
                    id=pid,
                    name=form.cleaned_data['name'],
                    city = form.cleaned_data['city'],
                    problem = form.cleaned_data['problem'],
                    solution = form.cleaned_data['solution']
                    )
                project_edit.save()
            except:
                form.add_error(None, 'Error. Please try again later.')
            if form.cleaned_data['video'] is not None:
                try:
                    project_video = Project(id=pid, intro_video = form.cleaned_data['video'])
                    project_video.save()
                except:
                    form.add_error('video', 'Error uploading video. Please use the suggested mp4 format. If this error continues, contact support.')
    else:
        context['form'] = projects.forms.ProjectChangeForm(initial={'name': project.name, 'problem': project.problem,'solution': project.solution, 'city': project.city})
        context['project'] = project
    return render(request, 'projects/edit.html', context)

def viewProject(request, slug):
    context={}
    try:
        project = Project.objects.get(slug=slug)
    except:
        raise Http404("Project not found") #project not found
    fundingrounds = FundingRound.objects.filter(project=project)
    if fundingrounds is None:
        raise Http404("This project is expired") # error in Project initialization - should never trigger
    fundinground = fundingrounds.latest()
    past_rounds = fundingrounds.exclude(pk=fundinground.pk)
    updates = Post.objects.get(project=project)
    context['project'] = project
    context['funding_round'] = fundinground
    context['past_rounds'] = past_rounds
    context['posts'] = updates
    return render(request, 'projects/view.html', context) #success redirect



    

