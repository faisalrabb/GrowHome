from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
# Create your views here.



@login_required
def index(request):
    context={}
    if method.request == 'GET':
        rdr=False
        #if a user visits this page without form submission
        pledges = Pledge.objects.filter(actor=request.user)[:5]
        if pledges is None:
            #if the user has no previous pledges to show information for
            rdr = True #redirect them to either their last viewed project or the homepage
        else:
            #if previous pledges exist, get the most recent unfulfilled pledge
            i = 0
            for pledge_ in pledges:
                contribution = Contribution.objects.filter(pledge=pledge_)
                if contribution is not None:
                    i += 1
                else:
                    pledge = pledge_ #this line fetches the most recent unfilfilled pledge and assigns it
                    break
            if i = pledges.size(): #if there are no unfilfilled pledges
                rdr = True #redirect the user
        if rdr == True: #if user needs to be redirected:
            try:
                #redirect them to the last project they were viewing
                project_id= request.session.get['pid']
                project = Project.objects.get(id=project_id)
                return redirect(project)
            except:
                #if no such project is found, redirect them to the homepage
                return redirect(reverse('feed:index'))
    else:
        form = contribute.forms.PaymentForm(request.POST)
        if form.is_valid():
            pledge = Pledge.objects.filter(actor=request.user, target=project)
            try:
                pid = request.session.get['pid']
                project = Project.objects.get(id=pid)
                funding_rounds = FundingRound.objects.filter(project=project)
                funding_round = funding_rounds.latest('created_at')
                pledge = Pledge.objects.filter(actor=request.user, target=funding_round)
                if pledge is not None:
                    pledge.latest().amount = form.cleaned_data['amount']
                else:
                    pledge = Pledge(
                        actor = request.user
                        funding_round = funding_round
                        amount = form.cleaned_data['amount']
                    )
                pledge.save()
            except:
                return HttpResponse("An error occured. Please go back to the project page and try again.")
    host = request.host()
    item_name = "Contribution to " + pledge.funding_round.project.__str__() + "'s latest funding round"
    paypal_dict = {
        'business': settings.PAYPAL_RECEIVER_EMAIL,
        'amount': pledge.amount,
        'item_name': item_name,
        'invoice': str(pledge.id),
        'currency_code': 'USD',
        'notify_url': 'https://{}{}'.format(host, reverse('paypal-ipn')),
        'return_url': 'https://{}{}'.format(host, reverse('contribute:done')),
        'cancel_return': 'https://{}{}'.format(host, reverse('contribute:canceled')),
    }
    context['form'] = PayPalPaymentsForm(initial=paypal_dict)
    context['pledge'] = pledge
    context['change_form'] = forms.PledgeForm(initial={'amount': pledge.amount})
    return render(request, 'contribute/process.html', context)
    #note about process: shows pledge info, change_form for changing the payment, which posts to the edit_pledge view, and the paypal payment form which posts to paypal

#@login_required
#def edit_pledge(request):
#    #ONLY ACCEPTS POST
#    if request.method == 'POST':
#        try:
#            #get the relevant pledge
#            pledge_id = request.session.get['pledge-id']
#            pledge = Pledge.objects.get(id=pledge_id)
#        except:
#            try:
#                #if pledge not found, redirect to last seen project, where they can make a new pledge
#                pid = request.session.get['pid']
#                project = Project.objects.get(id = pid)
#                return redirect(project)
#            except:
#                #if no previous project found in session redirect to index
#                return redirect(reverse('feed:index'))
#        if form.is_valid():
#            #if form is valid alter the amount in the pledge
#            pledge.amount = form.cleaned_data['amount']
#            pledge.save()
#            #redirect to index page where this pledge will be fetched by GET logic (by definition this pledge has to be the most recently unfilfilled one)
#            return redirect(reverse('contribute:index'))
#    return redirect(reverse('feed:index')) #failure/GET redirect

@csrf_exempt
def done(request):
    return render(request, 'contribute/done.html')
@csrf_exempt
def canceled(request):
    return render(request, 'contribute/canceled.html')

