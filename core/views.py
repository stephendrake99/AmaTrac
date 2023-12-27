

from django.db.models import Sum
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from transactions.models import *
from giftweb.models import *
from accounts.models import User
from django.core.paginator import Paginator
from core.models import *
from .forms import *

def home(request):
    users = User.objects.all()
    notify = Notification.objects.all()
    if not request.user.is_authenticated:
        return render(request, "core/index.html", {})
    else:
        user = request.user
        deposit = Diposit.objects.filter(user=user)
        deposit_sum = deposit.aggregate(Sum('amount'))['amount__sum']

        # Get the list of withdrawals
        withdrawals_list = Payment.objects.filter(user=request.user).order_by('-id')

        # Create a Paginator instance with the withdrawals list and the desired number of items per page
        paginator = Paginator(withdrawals_list, 5)  # Change '10' to your desired number of items per page

        # Get the current page number from the request's GET parameters
        page = request.GET.get('page')

        # Get the Page object for the current page
        withdrawals = paginator.get_page(page)
        withdrawal = Withdrawal.objects.filter(user=user)
        notify = Notification.objects.filter(user=user)

        cryptowithdrawal = CryptoWITHDRAW.objects.filter(user=user)
        withdrawal_sum = withdrawal.aggregate(Sum('amount'))['amount__sum']
        interest = Interest.objects.filter(user=user)
        interest_sum = interest.aggregate(Sum('amount'))['amount__sum']
        categories = Category.objects.all()
        form = SearchCourierForm(request.GET)
        couriers = None

        if form.is_valid():
            tracking_id = form.cleaned_data['tracking_id']

            # Perform the search based on the tracking_id
            couriers = Courier.objects.filter(tracking_id=tracking_id)

        context = {
            "user": user,
            "deposit": deposit,
            "notify": notify,
            "deposit_sum": deposit_sum,
            "withdrawal": withdrawal,
            "withdrawals": withdrawals,
            "withdrawal_sum": withdrawal_sum,
            "interest": interest,
            "interest_sum": interest_sum,

            "users": users,
            "form": form,
            "couriers": couriers,
            'categories': categories,
            "title": "Logistics"
        }

        return render(request, "core/transactions.html", context)

from django.http import JsonResponse

def homerz(request):
    if request.method == 'POST':
        form = SubscriberForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()

            # Add a success message
            messages.success(request, 'Your message was sent successfully.')

            # Return a JSON response indicating success
            return JsonResponse({'success': True})

    else:
        form = SubscriberForm()

    return render(request, 'core/index.html', {'form': form})

def products_by_category(request, category_name):
    category = Category.objects.get(name=category_name)
    products = category.products.all()
    
    # Paginate the products
    paginator = Paginator(products, 5)  # Show 12 products per page
    page = request.GET.get('page')
    products = paginator.get_page(page)
    
    context = {
        'category': category,
        'products': products
    }
    
    return render(request, 'giftweb/products_by_category.html', context)



def search_courier(request):
    form = SearchCourierForm(request.GET)
    couriers = None

    if form.is_valid():
        tracking_id = form.cleaned_data['tracking_id']

        # Perform the search based on the tracking_id
        couriers = Courier.objects.filter(tracking_id=tracking_id)

    return render(request, 'core/index.html', {'form': form, 'couriers': couriers})



@login_required
def payment_history(request):
    payments = Payment.objects.filter(user=request.user).order_by('-id')

    # Apply pagination with 7 entries per page
    paginator = Paginator(payments, 7)
    page_number = request.GET.get('page')  # Get the current page number from the request (e.g., query string parameter)

    # Get the corresponding page from the paginator
    page_obj = paginator.get_page(page_number)

    return render(request, 'core/transactions.html', {'page_obj': page_obj})
    
def about(request):
    return render(request, "core/about.html", {})  

def service(request):
    return render(request, "core/service.html", {})

def contact_us(request):
    return render(request, "core/contact_us.html", {})



@login_required
def confirm(request):
    payment = Withdrawal.objects.filter(user=request.user).order_by('-id').first()
    return render(request, 'core/confirm.html', {'payment': payment})


@login_required
def inter_confirm(request):
    payment = Withdrawal_internationa.objects.filter(user=request.user).order_by('-id').first()
    return render(request, 'core/inter_confirm.html', {'payment': payment})


def confirm_password(request):
    return render(request, "core/confirm_password.html", {})
