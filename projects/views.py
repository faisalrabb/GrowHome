from django.shortcuts import render
from feed.models import Post
from projects.forms import ProjectForm, FundingRoundForm
from projects.models import FundingRound, Project
from account.models import User, Entrepeneur
from django.contrib.auth.decorators import login_required
from contribute.forms import PledgeForm
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
                    category = form.cleaned_data['category'],
                    info = form.cleaned_data['info'],
                    country = entrepeneurInstance.country,
                    city = form.cleaned_data['city'],
                    intro_video = form.cleaned_data['video'],
                    photo = form.cleaned_data['photo'],
                    looking_for = form.cleaned_data['looking_for']
                )
                this_project.save()
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
    rnumber = 0
    try:
        entrepeneur = Entrepeneur.objects.get(user=request.user)
        project = Project.objects.get(pk=pid, creator=entrepeneur)
        fundingrounds = FundingRound.objects.filter(project=project)
        if fundingrounds is not None:
            fr = fundingrounds.latest()
            rnumber = fr.round_number
            if fr.goals_finished = False:
                return redirect(project)
    except: 
        return HttpResponseRedirect(reverse('feed:index')) #non-owner redirect
    if request.method == 'POST':
        form = projects.forms.FundingRoundForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                frnumber = fnumber + 1
                fundinground = FundingRound(
                    project = project,
                    funding_goal = form.cleaned_data['funding_goal'],
                    round_number = frnumber,
                    info = form.cleaned_data['info'],
                    video = form.cleaned_data['video'],
                    note = form.cleaned_data['note'],
                )
                fundinground.save()
                goals = [form.cleaned_data['goal_1'], form.cleaned_data['goal_2'], form.cleaned_data['goal_3']]
                for goal_ in goals:
                    if goal_ is not None:
                        goal = Goal(text=goal_, funding_round = fundinground)
                        goal.save()
                    return redirect(project) #success redirect 
            except:
                form.add_error(None, 'Error saving funding round. Please try again later. If this problem persists, contact support')
        context['form'] = form
    else:
        context['form'] = projects.forms.FundingRoundForm()
        context['project'] = project
    return render(request, '/projects/newfundinground.html', context) #retry/get redirect

@login_required
def editFundingRound(request):
    try:
        creator = Enterepeneur.objets.get(user=request.user)
        pid = request.session['pid']
        project = Project.objects.get(creator=creator, id=pid)
        funding_round=FundingRound.objects.filter(project=project).latest()
    except:
        return redirect(reverse('feed:index'))
    if request.method == 'POST':
        form=projects.forms.FundingRoundUpdateForm(request.POST, request.FILES)
        if form.is_valid() and form.has_changed():
            try:
                edit_fr= FundingRound(
                    id=funding_round.id,
                    funding_goal=form.cleaned_data['funding_goal'],
                    info = form.cleaned_data['info'],
                    note = form.cleaned_data['note']
                )
                if form.cleaned_data['video'] is not None:
                    edit_fr.video= form.cleaned_data['video']
                edit_fr.save()
                return redirect(project)
            except:
                form.add_error(None, 'Could not successfuly edit project. Please check that the changes did not take place and try again.')   
        context['form'] = form
    else:
        context['form'] = projects.forms.FundingRoundUpdateForm(initial={'funding_goal':funding_round.funding_goal, 'info': funding_round.info, 'note': funding_round.note})
    return render(request,'projects/editfundinground.html', context)
    
        



@login_required
def editProject(request, pid):
    try:
        creator = Entrepeneur.objects.get(user=request.user)
        project= Project.objects.get(pk=pid, creator=creator)
    except:
        return redirect(reverse('feed:index')) #project not found error
    context={}
    if request.method == 'POST':
        form = projects.forms.ProjectForm(request.POST, request.FILES)
        if form.is_valid() and form.has_changed():
            try:
                fail=0
                project_edit = Project(
                    id=pid,
                    name=form.cleaned_data['name'],
                    city = form.cleaned_data['city'],
                    problem = form.cleaned_data['problem'],
                    solution = form.cleaned_data['solution'],
                    looking_for = form.cleaned_data['looking_for']
                    )
                    if form.cleaned_data['video'] is not None:
                            project_edit.intro_video = form.cleaned_data['video']
                    if form.cleaned_data['photo'] is not None:
                            project_edit.photo = form.cleaned_data['photo'] 
                    project_edit.save()
            except:
                form.add_error(None, 'Error. Please try again later.')
    else:
        context['form'] = projects.forms.ProjectForm(initial={'name': project.name, 'problem': project.problem,'solution': project.solution, 'city': project.city, 'looking_for': project.looking_for})
        context['project'] = project
    return render(request, 'projects/edit.html', context)

def viewProject(request, slug):
    context={}
    try:
        project = Project.objects.get(slug=slug)
        project.views += 1
    except:
        raise Http404("Project not found") #project not found
    fundingrounds = FundingRound.objects.filter(project=project)
    if fundingrounds is not None:
        fundinground = fundingrounds.latest()
        context['funding_round'] = fundinground
        past_rounds = fundingrounds.exclude(pk=fundinground.pk)
        context['past_rounds'] = past_rounds
    updates = Post.objects.filter(project=project) 
    context['project'] = project
    context['posts'] = updates
    request.session['pid'] = project.id
    if request.user.is_authenticated:
        if request.user == project.creator.user:
            context['add_goal_form'] = projects.forms.AddGoalForm()
            context['post_form'] = feed.forms.PostForm()
            #project creator specific stuff
        else:
            context['pledge_form'] = contribute.forms.PledgeForm()
    return render(request, 'projects/view.html', context) #success redirect

@login_required
def addGoal(request):
    try:
        ent = Entrepeneur.objects.get(user=request.user)
        pid = request.session['pid']
        proj = Project.objects.get(id=pid, creator=ent)
    except:
        return redirect(reverse('feed:index'))
    if ent != proj.creator:
        return redirect(proj)
    #end of authentication/permission check
    if request.method == 'POST':
        form = projects.forms.AddGoalForm(request.POST)
        if form.is_valid():
            latest_funding_round = FundingRound.objects.filter(project=proj).latest()
            goal = Goal(
                text=form.cleaned_data['text'],
                funding_round = latest_funding_round
            )
            goal.save()
    return redirect(proj)
    



    

