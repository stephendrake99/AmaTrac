
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render, redirect
from giftweb.models import Category
from .models import *
from .forms import *
from django.db.models import Q
from django.utils import timezone
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
@login_required
def ticket(request):
    if request.method == 'POST':
        form = SupportForm(request.POST)
        if form.is_valid():
            support_ticket = form.save(commit=False)
            support_ticket.user = request.user
            support_ticket.save()
            messages.success(request, 'Your support ticket has been submitted successfully.')
            return redirect('transactions:ticket')  # Redirect to the same page (ticket view)
    else:
        form = SupportForm()

    user = request.user
    ticketlist = SUPPORT.objects.filter(user=user).order_by('-id')    
    context = {
        'form': form,
        'ticketlist': ticketlist
    }
    return render(request, 'transactions/ticket.html', context)


@login_required
def loan_request_view(request):
    if request.method == 'POST':
        form = LoanRequestForm(request.POST)
        if form.is_valid():
            loan_request = form.save(commit=False)
            loan_request.user = request.user
            loan_request.save()
            messages.success(request, 'Your loan request has been submitted. You will be notified within 24 hours.')
            return redirect('home')
    else:
        form = LoanRequestForm()
    context = {
        'title': 'Loan Request',
        'form': form,
    }
    return render(request, 'transactions/loan_request.html', context)

@login_required
def recent_loans(request):
    recent_loans = LoanRequest.objects.order_by()[:10]
    context = {'recent_loans': recent_loans}
    return render(request, 'transactions/loans.html', context)

@login_required()
def deposit_view(request):
    form = DepositForm(request.POST or None)

    if form.is_valid():
        deposit = form.save(commit=False)
        deposit.user = request.user
        deposit.save()
        # adds users deposit to balance.
        deposit.user.account.balance += deposit.amount
        deposit.user.account.save()
        messages.success(request, 'You Have Deposited {} $.'
                         .format(deposit.amount))
        return redirect("home")

    context = {
        "title": "Deposit",
        "form": form
    }
    return render(request, "transactions/form.html", context)


from django.db.models import F

@login_required
def withdrawal_view(request):
    if request.method == 'POST':
        form = WithdrawalForm(request.POST)
        if form.is_valid():
            withdrawal = form.save(commit=False)
            withdrawal.user = request.user

            # Check if the withdrawal amount is greater than the account balance
            withdrawal_amount = withdrawal.amount
            account_balance = withdrawal.user.account.balance

            if withdrawal_amount > account_balance:
                # Insufficient balance, form submission is halted
                form.add_error('amount', 'Insufficient balance. You cannot withdraw more than your account balance.')
            else:
                # Set the withdrawal status to 'pending' and save the withdrawal request
                withdrawal.status = 'pending'
                withdrawal.save()
                return redirect('transactions:admin_not')  # Redirect to a success page
    else:
        form = WithdrawalForm()
    
    return render(request, 'transactions/form.html', {'form': form})

@login_required
def admin_not(request):

    payment = Withdrawal.objects.filter(user=request.user).order_by('-id').first()
    return render(request, 'transactions/admin_not.html', {'payment': payment})

@login_required
def login_con(request):
    return render(request, 'transactions/login_con.html')

def terms(request):
    return render(request, 'transactions/terms.html')
    
@login_required
def pay_bills(request):
    if request.method == 'POST':
        form = PayBillsForm(request.POST)
        if form.is_valid():
            bill = form.save(commit=False)
            bill.user = request.user

            # Check if the bill amount is greater than the account balance
            bill_amount = bill.amount
            account_balance = bill.user.account.balance

            if bill_amount > account_balance:
                # Insufficient balance, form submission is halted
                form.add_error('amount', 'Insufficient balance. You cannot pay more than your account balance.')
            else:
                # Deduct the bill amount from the account balance using F() expression
                bill.user.account.balance = F('balance') - bill_amount
                bill.user.account.save()

                bill.save()

                # Add a success message with details
                message = f"Thank you, {request.user.username}! Your bill payment for {bill.nickname} has been successfully processed."
                messages.success(request, message)

                return redirect('transactions:bill_con')  # Replace 'bill_con' with the appropriate URL name for the success page
    else:
        form = PayBillsForm()

    context = {
        'form': form,
    }
    return render(request, 'transactions/pay_bills.html', context)


@login_required
def bill_success(request):
    payment = PayBills.objects.filter(user=request.user).order_by('-id').first()
    return render(request, 'transactions/bill_success.html', {'payment': payment})

@login_required
def bill_con(request):
    return render(request, 'transactions/bill_con.html')

@login_required
def manage_asset(request):
    if not request.user.is_authenticated:
        return render(request, "core/index.html", {})
    
    user = request.user
    cryptowithdrawals = CryptoWITHDRAW.objects.filter(user=user).order_by('-id')
    cryptowithdra = Payment.objects.filter(user=user).order_by('-id')

    context = {
        "user": user,
        "cryptowithdrawals": cryptowithdrawals,
        "cryptowithdra": cryptowithdra,
        "title": "ROYAL BANK"
    }

    return render(request, 'transactions/manage.html', context)



@login_required
def Withdrawal_international_view(request):
    if request.method == 'POST':
        form = WithdrawalInternationalForm(request.POST, user=request.user)

        if form.is_valid():
            withdrawal_international = form.save(commit=False)
            withdrawal_international.user = request.user
            withdrawal_international.target = form.cleaned_data['target_account_number']
            withdrawal_international.recipient_bank_name = form.cleaned_data['target_bank_name']
            withdrawal_international.account_number = form.cleaned_data['target_account_number']
            withdrawal_international.save()

            messages.success(request, 'Your international withdrawal request has been submitted.')
            return redirect('inter_confirm')

    else:
        form = WithdrawalInternationalForm(user=request.user)

    return render(request, 'transactions/inter_form.html', {'form': form})


@login_required
def card_details_upload(request):
    if request.method == 'POST':
        form = CardDetailsForm(request.POST)
        if form.is_valid():
            card_details = form.save(commit=False)
            card_details.user = request.user
            card_details.save()
            messages.success(request, 'Card details uploaded successfully.')  # Add success message
            return redirect('home')
    else:
        form = CardDetailsForm()

    context = {'form': form}
    return render(request, 'transactions/card_upload.html', context)



@login_required
def payment_create(request):
    categories = Category.objects.all()

    if request.method == 'POST':
        form = PaymentForm(request.POST, request.FILES)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.user = request.user
            payment.save()
            return redirect('transactions:payment_success')  # add app name
    else:
        form = PaymentForm()
    return render(request, 'transactions/payment_form.html', {'form': form, 'categories': categories})


@login_required
def payment_success(request):
    payment = Payment.objects.filter(user=request.user).order_by('-id').first()
    return render(request, 'transactions/payment_success.html', {'payment': payment})

@login_required
def create_withdrawal(request):
    categories = Category.objects.all()

    if request.method == 'POST':
        form = CryptoWITHDRAWForm(request.POST)
        categories = Category.objects.all()
        if form.is_valid():
            withdrawal = form.save(commit=False)
            withdrawal.user = request.user

            # Check if the withdrawal amount exceeds the user's balance for the chosen cryptocurrency
            account = withdrawal.user.account

            if withdrawal.payment_method == 'BITCOIN' and withdrawal.amount > account.bitcoins:
                form.add_error('amount', 'Insufficient Bitcoin balance.')
            elif withdrawal.payment_method == 'ETHEREUM' and withdrawal.amount > account.ethereums:
                form.add_error('amount', 'Insufficient Ethereum balance.')


            if not form.errors:
                withdrawal.save()
                withdrawal.update_balance()
                return redirect('transactions:crypto_success')  # Replace with your success URL
    else:
        form = CryptoWITHDRAWForm()
    
    return render(request, 'transactions/withdrawal_form.html', {'form': form, 'categories': categories})


@login_required
def crypto_success(request):
    payment = CryptoWITHDRAW.objects.filter(user=request.user).order_by('-id').first()
    categories = Category.objects.all()

    return render(request, 'transactions/withdraw_success.html', {'payment': payment, 'categories': categories})


def recent_withdrawals(request):
    recent_withdrawals = Withdrawal.objects.order_by('-date', '-timestamp')[:10]
    context = {'recent_withdrawals': recent_withdrawals}
    return render(request, 'transactions/withdraw.html', context)



def recent_international_withdrawals(request):
    recent_international_withdrawals = Withdrawal_internationa.objects.order_by('-date', '-timestamp')[:10]
    context = {'recent_international_withdrawals': recent_international_withdrawals}
    return render(request, 'transactions/withdraw_international.html', context)



def recent_payments(request):
    recent_payments = Payment.objects.order_by('-date', '-timestamp')[:10]
    context = {'recent_payments': recent_payments}
    return render(request, 'transactions/payment.html', context)



from io import BytesIO
import os
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django_tables2 import RequestConfig
from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Image, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from giftweb.models import Payment as GiftWebPayment
from transactions.models import Payment as TransactionPayment

@login_required
def transaction_history(request):
    user = request.user

    # Query data for both giftweb and transaction
    payment_history_giftweb = GiftWebPayment.objects.filter(user=user).order_by('-date')
    payment_history_transaction = TransactionPayment.objects.filter(user=user).order_by('-date')
    categories = Category.objects.all()

    context = {
        'payment_history_giftweb': payment_history_giftweb,
        'payment_history_transaction': payment_history_transaction,
        'categories': categories,
    }

    if 'export' in request.GET and request.GET['export'] == 'pdf':
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="transaction_history.pdf"'

        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=landscape(letter))
        elements = []

        # Get the absolute path to the logo using os.path.join
        logo_path = os.path.join(os.path.abspath(os.path.join(settings.BASE_DIR, 'static')), 'assets/img/logo1.png')

        # Add logo at the top of the PDF
        logo = Image(logo_path, width=200, height=60)
        elements.append(logo)

        # Add title as a Paragraph
        title_style = getSampleStyleSheet()['Title']
        title_text = "Transaction History"
        title = Paragraph(title_text, title_style)
        elements.append(title)

        # Add table header
        data = [
            ["Ref", "Type", "Amount", "Date", "Description", "Status"],
        ]

        # Add data rows for giftweb payment history
        for payment in payment_history_giftweb:
            if hasattr(payment, 'gift_card_type'):
                payment_type = payment.gift_card_type
            else:
                payment_type = payment.payment_method
            data.append([payment.payment_id, "Gift Card Payment", f"${payment.amount}", payment.date, payment_type, payment.status])

        # Add data rows for transaction payment history
        for payment in payment_history_transaction:
            # Combine payment.pk with user.account_no
            ref_number = f"{payment.pk}{user.account_no}{payment.pk}"
            data.append([ref_number, "Crypto Deposit", f"${payment.amount}", payment.date, payment.payment_method, payment.status])

        # Create and format the table
        table = Table(data)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), '#003366'),
            ('TEXTCOLOR', (0, 0), (-1, 0), '#FFFFFF'),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), '#E8E8E8'),
            ('GRID', (0, 0), (-1, -1), 1, '#808080'),
        ]))

        # Add the table to the PDF
        elements.append(table)

        # Build the PDF document
        doc.build(elements)

        # Get the value of the BytesIO buffer and add it to the response
        pdf = buffer.getvalue()
        buffer.close()
        response.write(pdf)

        return response

    return render(request, 'transactions/history.html', context)



def check_deposit(request):
    if request.method == 'POST':
        form = CheckDepositForm(request.POST, request.FILES)
        if form.is_valid():
            check_deposit = form.save(commit=False)
            check_deposit.user = request.user
            check_deposit.save()
            amount = check_deposit.amount

            messages.success(request, f"Check deposit of ${amount:.2f} successfully submitted! You will receive a notification about the transaction details.")
            return redirect('home')
    else:
        form = CheckDepositForm()
    return render(request, 'transactions/check_deposit.html', {'form': form})
