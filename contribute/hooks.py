from paypal.standard.models import ST_PP_COMPLETED
from paypal.standard.ipn.signals import valid_ipn_received, invalid_ipn_received
from contribute.models import Contribution, Pledge, PaymentError

def successful_payment(sender, **kwargs):
    ipn_obj = sender
    if ipn_obj.payment_status == ST_PP_COMPLETED:
        # Check that the receiver email is the same we previously (The user could tamper with that fields on the payment form before it goes to PayPal)
        if ipn_obj.receiver_email != settings.PAYPAL_RECEIVER_EMAIL:
            # Not a valid payment - exit function
            new_error = PaymentError(
                pledge_id = int(ipn_obj.invoice),
                ipn_sender_email = ipn_obj.sender_email,
                paypal_invoice = ipn_obj.txn_id,
                amount_paid = ipn_obj.mc_gross,
                currency = ipn_obj.mc_currency,
                description = "Receiver e-mail does not match GrowHome business e-mail (likely due to form tampering). Invalid payment. No contribution has been added. No further action required."
            )
            new_error.save()
            return 
        try:
            #try to get the pledge from the invoice id
            pledge = Pledge.objects.get(id=int(ipn_obj.invoice))
        except:
            #pledge not found
            new_error = PaymentError(
                pledge_id = int(ipn_obj.invoice),
                ipn_sender_email = ipn_obj.sender_email,
                paypal_invoice = ipn_obj.txn_id,
                description = "Pledge not found, meaning there's no info about which project this is for. The amount_paid attribute represents the amount this user has paid. This has not recorded as a new Contribution, but the funds have been transferred to us. Check user's actions to figure out who this contribution is for, and make appropriate changes to that project's finances.",
                amount_paid = ipn_obj.mc_gross,
                currency = ipn_obj.mc_currency,
            )
            new_error.save()
            return
        if ipn_obj.mc_gross < 0:
            cnf_bool = False
            try:
                contribution = Contribution.objects.get(pledge=pledge)
                old_amount = contribution.amount
            except:
                old_amount = 0
                cnf_bool = True
            reversal = PaymentReversal(
                contribution= contribution,
                old_amount = old_amount,
                new_amount = old_amount + ipn_obj.mc_gross,
                change = ipn_obj.mc_gross,
                contribution_not_found = cnf_bool
            )
            reversal.save()
        else: 
            conflicts = Contribution.objects.filter(pledge=pledge)
            if conflicts is not None:
                #the pledge has already been fulfilled - duplicate payment
                new_error = PaymentError(
                    pledge_id = int(ipn_obj.invoice),
                    ipn_sender_email = ipn_obj.sender_email,
                    paypal_invoice = ipn_obj.txn_id,
                    previous_contribution = conflicts.first(),
                    description="The pledge has already been fulfilled. This could be a duplicate payment. This action has been recorded as a new contribution, possibly with different attributes for amount, currency, paypal invoice. Make sure this is an intended action; if all seems normal, ignore this.",
                )
                new_error.save() 
        contribution = Contribution(
            actor = pledge.actor,
            funding_round = pledge.funding_round,
            project = pledge.funding_round.project,
            currency = ipn_obj.mc_currency,
            amount_total = ipn_obj.mc_gross, 
            amount_after_paypal_fee = ipn_obj.payment_fee,
            amount_final = (ipn_obj.payment_fee * 0.95),
            gh_fee_amount = (ipn_obj.payment_fee * 0.05),
            pledge = pledge,
            ipn_sender_email = ipn_obj.sender_email,
            paypal_invoice = ipn_obj.txn_id
        )
        contribution.save()
        pledge.fulfilled = True
        pledge.save()
    else:
        #payment status =/= complete
        non_completed_payment = NonCompletePayment(
            pledge_id = int(ipn_obj.invoice),
            ipn_sender_email = ipn_obj.sender_email,
            paypal_invoice = ipn_obj.txn_id,
            description = "This payment is not completed. It may be pending, canceled, rejected, reversed, etc. No money has been added to our account balance. Check the PayPal website with this transaction's ID to see if any further action is needed.",
            amount_paid = ipn_obj.mc_gross,
            currency = ipn_obj.mc_currency
        )
        non_completed_payment.save()


valid_ipn_received.connect(successful_payment)