from django_cron import CronJobBase, Schedule
from contribute.models import FundingReport, Contribution
from projects.models import Project, FundingRound
from django.core.mail import send_mail
from django.conf import settings

class FundingReport(CronJobBase):
    RUN_EVERY_MINS = 120 # every two hours

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'contribute.funding_report'    # a unique code

    def do(self):
        now = datetime.datetime.now()
        reports = FundingReport.objects.all()
        if reports is not None:
            last_report = reports.latest() 
            time_since = now - last_report.time
            if time_since.days < 7:
                return
            contributions = Contribution.object.filter(created_at__gt=last_report.time, created_at__lte=now)
        else:
            contributions = Contribution.objects.all()
        if contributions is None:
            return
        text = "key: project, username, total funds before Paypal fees, total funds after Paypal fees (before GH fees), total fees collected by GrowHome, total funds to be transfered to project \nNote: The total amount *to be transfered* to a project is not equal to the total amount *received by* the project due to WorldRemit fees\n\n_____________________\n"
        receivers = []
        #make list of receivers
        for contribution in contributions:
            if contribution.project not in receivers:
                receivers.append(contribution.project)
        row_number = 0
        #generate CSV line for each receiver
        for receiver in receivers:
            row_number += 1
            username = receiver.creator.user.username
            #(re-)set the variables used
            total_before_paypal_fees = 0
            total_after_paypal_fees = 0
            total_to_receive = 0
            total_gh_fees = 0
            #filter the contributions to only get projects from the receiver
            contribs = contributions.filter(project=receiver)
            for i in contribs:
                #adding amounts from each contribution made to receiver
                total_before_paypal_fees += i.amount_total
                total_after_paypal_fees += i.amount_after_paypal_fee
                total_to_receive += i.amount_final
                total_gh_fees += i.gh_fee_amount
            #compose CSV line with this information, add to text
            text += row_number + ': ' + receiver.__str__() +', ' + receiver.creator.user.username + ', ' + str(total_before_paypal_fees) + ', ' + str(total_after_paypal_fees) + ', ' + str(total_gh_fees) + ', ' + str(total_to_receive) + '\n'
        #save report model
        new_report = FundingReport(time=now, text=text)
        new_report.save()
        #send info in an email
        send_email(
            'Fundraising overview for the last 7 days', 
            text,
            settings.EMAIL_HOST_USER,
            ['faisal.rabbani@mail.mcgill.ca'],
            fail_silently=True
            )



            
        