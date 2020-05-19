from paypal.standard.models import ST_PP_COMPLETED
from paypal.standard.ipn.signals import valid_ipn_received
from contribute.models import Contribution, Pledge, PaymentError

def successful_payment(sender, **kwargs):
    ipn_obj = sender
    if ipn_obj.payment_status == ST_PP_COMPLETED:
        # Check that the receiver email is the same we previously (The user could tamper with that fields on the payment form before it goes to PayPal)
        if ipn_obj.receiver_email != settings.PAYPAL_RECEIVER_EMAIL:
            # Not a valid payment - exit function
            new_error = PaymentError(
                pledge_id = int(ipn_obj.invoice)
                ipn_sender_email = ipn_obj.sender_email
                paypal_invoice = ipn_obj.txn_id
                amount_paid = ipn_obj.mc_gross
                currency = ipn_obj.mc_currency
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
                pledge_id = int(ipn_obj.invoice)
                ipn_sender_email = ipn_obj.sender_email
                paypal_invoice = ipn_obj.txn_id
                description = "Pledge not found, meaning there's no info about which project this is for. The amount_paid attribute represents the amount this user has paid. This has not registered as a payment in the Contributions page. Check user's actions to figure out who this contribution is for, and make appropriate changes."
                amount_paid = ipn_obj.mc_gross
                currency = ipn_obj.mc_currency
            )
            new_error.save()
            return
        conflict = Contribution.objects.filter(pledge=pledge)
        if conflict is not None:
            #the pledge has already been fulfilled - duplicate payment
            new_error = PaymentError(
                pledge_id = int(ipn_obj.invoice)
                ipn_sender_email = ipn_obj.sender_email
                paypal_invoice = ipn_obj.txn_id
                previous_contribution = conflict.first()
                description="The pledge has already been fulfilled. This could be a duplicate payment. Contact the email associated and ask if this was an intended action. This action has been recorded as a new contribution, possibly with different attributes for amount, currency, paypal invoice"
            )
            new_error.save() 
        # ALSO: for the same reason, you need to check the amount
        # received, `custom` etc. are all what you expect or what
        # is allowed.
        # Undertake some action depending upon `ipn_obj`.
        if ipn_obj.mc_gross < 0:
            try:
                contribution = Contribution.objects.get(pledge = pledge)
            except:
                #contribution not found, error reported 
                new_error = PaymentError(
                    pledge_id = int(ipn_obj.invoice),
                    ipn_sender_email = ipn_obj.sender_email,
                    paypal_invoice = ipn_obj.txn_id,
                    description = "This payment is a reversal (full or partial refund) done by PayPal. The contribution was not found in the database. Find the contribution this is associated with, and subtract that amount from the project's funds. This error is extremely rare and should be reported if ever triggered.",
                    amount_paid = ipn_obj.mc_gross,
                    currency= ipn_obj.mc_currency,
                )
                new_error.save()
                return
            old_amount = contribution.amount
            contribution.amount = contribution.amount + ipn_obj.mc_gross
            #recording successful reversal
            reversal = PaymentReversal(
                contribution= contribution,
                old_amount = old_amount,
                new_amount = old_amount + ipn_obj.mc_gross,
                change = ipn_obj.mc_gross
            )
            reversal.save()
        else:
            #payment amount is positive - i.e. not a change to an existing payment
            contribution = Contribution(
                user = pledge.user,
                funding_round = pledge.funding_round,
                currency = ipn_obj.mc_currency,
                amount = ipn_obj.mc_gross, 
                pledge = pledge,
                ipn_sender_email = ipn_obj.sender_email,
                paypal_invoice = ipn_obj.txn_id
            )
        contribution.save()
    else:
        #payment failed
        failed_payment = FailedPayment(
            pledge_id = int(ipn_obj.invoice)
            ipn_sender_email = ipn_obj.sender_email
            paypal_invoice = ipn_obj.txn_id
            description = "This payment did not go through. No further action required, this information is just for record-keeping purposes."
            amount_paid = ipn_obj.mc_gross
            currency = ipn_obj.mc_currency
        )
        failed_payment.save()

valid_ipn_received.connect(successful_payment)