from django.shortcuts import render
from projects.forms import ProjectForm, FundingRoundForm
from projects.models import FundingRound, Project
from account.models import User, Entrepeneur

# Create your views here.

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
                return HttpResponseRedirect(reverse(projects.views.viewProject, kwargs={'pid': pid})) #success redirect
            except IntegrityError:
                form.add_error('project', 'Project name already exists.')
        context['form'] = form
    else:
        context['form'] = projects.forms.ProjectForm()
    return render(request,'projects/new.html', context) #try again redirect


#funding round: 1. check active project, 2. check last funding round status (closed, 3 goals accomplished)

def newFundingRound(request, pid):
    context={}
    try:
        entrepeneur = Entrepeneur.objects.get(user=request.user)
        project = Project.objects.get(pk=pid)
        fundingrounds = FundingRound.objects.filter(project=project)
        if fundingrounds is None:
            return HttpsResponse("Previous funding rounds not found") #Error in project initialization. 
        else:
            fundinground = fundingrounds.latest()
        if project.creator != entrepeneur:
            return HttpResponse("Unauthorized action") #project not created by user - shouldn't trigger unless malicious attempt
    except: 
        return HttpResponseRedirect(reverse('feed:index')) #non-entrepeneur redirect
    if request.method == 'POST':
        form = projects.forms.FundingRoundForm(request.POST, request.FILES)
        if not (fundinground.goal_1_finished and fundinground.goal_2_finished and fundinground.goal_3_finished):
            form.add_error(None, "Your previous funding round has unaccomplished goals. Mark these as completed in order to start a new funding round. If you believe this is an error, please contact support.")
        else if form.is_valid():
            try:
                fundinground = FundingRound(
                    project = project
                    funding_goal = 
                    goal_1 = 
                    goal_2 = 
                    goal_3 =
                    info = 
                    video = 
                    note = 
                )
                fundinground.save()
                return HttpResponseRedirect(reverse(projects.views.viewProject, kwargs={'pid': pid})) #success redirect
            except IntegrityError:
                form.add_error(None, 'Error saving funding round. Please try again later. If this problem persists, contact support')
    else:
        context['form'] = projects.forms.FundingRoundForm()
    return render(request, '/projects/newfundinground.html', context) #retry redirect
    

