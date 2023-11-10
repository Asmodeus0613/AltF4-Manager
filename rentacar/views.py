from urllib import response
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import logout
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.shortcuts import render
from django.shortcuts import render
from .models import Car, Order
from django.shortcuts import render, get_object_or_404
from django.forms import ModelForm
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Order, Car
from django.shortcuts import render, redirect, get_object_or_404
from datetime import datetime
import random
import string
import json

@csrf_exempt
def create_order(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        car_id = data['carID']
        start_date = data['startDate']
        end_date = data['endDate']
        duration = data['duration']
        status = data.get('status', 0)  # Default status is 0 if not provided

        # Retrieve the Car object
        car = Car.objects.get(pk=car_id)

        # Generate a random order number
        order_number = ''.join(random.choices(string.digits, k=8))

        # Calculate the total price for the whole duration
        total_price = car.carRate * float(duration)

        # Create the Order object
        order = Order.objects.create(
            orderNumber=order_number,
            userid=request.user,
            carid=car,
            carName=car.carName,
            startDate=start_date,
            endDate=end_date,
            total=total_price,
            duration=duration,
            status=status,  # Set the status
        )

        car.status = 1
        car.save()

        response_data = {
            'success': True,
            'orderNumber': order.orderNumber,
            'carName': car.carName,
            'carRate': car.carRate,
            'startDate': start_date,
            'endDate': end_date,
            'totalPrice': total_price,
            'status': status,  # Include the status in the response
        }

        return JsonResponse(response_data)
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request method'})


from django.shortcuts import render, redirect
from .forms import CarForm

def get_username(request):
    if request.user.is_authenticated:
        username = request.user.username
        return JsonResponse({"username": username})
    else:
        return JsonResponse({"error": "User not authenticated"})


def landing_page(request):
    return render(request, "RentACar/landingpage.html")


def home(request):
    user_is_admin = request.user.is_staff

    context = {
        "user_is_admin": user_is_admin,
    }
    return render(request, "RentACar/homepage.html", context)


def viosfinal(request):
    # Add your logic for the 'viosfinal' view here
    return render(request, "RentACar/viosfinal.html")


def ertigafinal(request):
    # Add your logic for the 'viosfinal' view here
    return render(request, "RentACar/ertigafinal.html")


def terms_and_conditions(request):
    return render(request, "RentACar/terms_and_conditions.html")


def car_management(request):
    # Check if the user is an admin
    user_is_admin = request.user.is_staff
    # Fetch the list of cars from the database
    cars = Car.objects.all()
    context = {
        "user_is_admin": user_is_admin,
        "cars": cars,  # Add the 'cars' context variable
    }
    return render(request, "RentACar/carman.html", context)


def cars(request):
    car = Car.objects.all()
    return render(request, "RentACar/car_list.html", {"cars": car})


def about(request):
    return render(request, "RentACar/about.html")


@login_required
def carlists(request):
    return render(request, "RentACar/login.html")


@csrf_exempt
def check_availability(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        car_id = data['carID']
        start_date = data['startDate']
        end_date = data['endDate']

        # Convert start_date and end_date to datetime objects
        start_date = datetime.strptime(start_date, "%Y-%m-%d")
        end_date = datetime.strptime(end_date, "%Y-%m-%d")

        # Check for overlapping reservations
        overlapping_reservations = Order.objects.filter(
            carid=car_id,
            startDate__lte=end_date,
            endDate__gte=start_date
        )

        if overlapping_reservations.exists():
            is_available = False
            conflicting_reservation = overlapping_reservations.first()
            message = f"Car is not available during the selected dates. It's rented from {conflicting_reservation.startDate} to {conflicting_reservation.endDate}."
        else:
            is_available = True
            message = "Car is available during the selected dates."

        return JsonResponse({'available': is_available, 'message': message})

def cart(request, car_id):
    car = get_object_or_404(Car, CarID=car_id)
    return render(request, "RentACar/cart.html", {"car": car})


class CustomLoginView(LoginView):
    template_name = "RentACar/login.html"
    redirect_authenticated_user = True
    success_url = reverse_lazy("homepage")

    def get_success_url(self):
        return self.success_url

    def form_invalid(self, form):
        messages.error(self.request, "Invalid username or password. Please try again.")
        return super().form_invalid(form)


def car_detail(request, car_id):
    car = get_object_or_404(Car, CarID=car_id)
    status_text = "Rent" if car.status != 1 else "Reserve"
    return render(request, "RentACar/car_detail.html", {"car": car, "status_text": status_text})



def register(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")

        if User.objects.filter(Q(username=username) | Q(email=email)).exists():
            messages.error(request, "Username or email already exists.")
            return render(request, "RentACar/register.html")

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
        )
        user.save()
        return redirect("login")
    return render(request, "RentACar/register.html")


def logout_view(request):
    logout(request)
    return redirect("login")


class CarForm(ModelForm):
    class Meta:
        model = Car
        fields = ["carName", "carType", "carDescription", "carRate"]


from .forms import CarForm  # Import the CarForm

from django.shortcuts import render, get_object_or_404, redirect
from .models import Car
from .forms import CarForm

@login_required
def add_car(request):
    if request.method == "POST":
        form = CarForm(request.POST, request.FILES)
        if form.is_valid():
            car = form.save(commit=False)  # Create a car object but don't save it yet
            car.save()  # Save the car object to generate a CarID
            # Handle the image file upload
            if 'carImage' in request.FILES:
                car.carPic = request.FILES['carImage']
                car.save()
            return redirect("car_management")
    else:
        form = CarForm()

    return render(request, "RentACar/add_car.html", {"form": form})



def update_car(request, car_id):
    # Retrieve the car object from the database
    car = get_object_or_404(Car, CarID=car_id)

    if request.method == "POST":
        form = CarForm(request.POST, request.FILES, instance=car)
        if form.is_valid():
            car = form.save()  # Save the updated data to the database
            # Update availability (status) based on the form's status field
            if 'status' in form.cleaned_data:
                car.status = 0 if form.cleaned_data['status'] == 0 else 1
                car.save()
            return redirect('car_management')  # Redirect to the car management page
    else:
        form = CarForm(instance=car)

    context = {
        'form': form,
        'car': car,
    }
    return render(request, 'RentACar/update_car.html', context)


def delete_car(request, car_id):
    car = get_object_or_404(Car, id=car_id)
    if request.method == "POST":
        car.delete()
        return redirect("car_management")

    return render(request, "delete_car.html", {"car": car})

from django.http import JsonResponse

def reserve_car(request, car_id):
    return redirect('car_detail', car_id=car_id)

def order_list(request):
    user = request.user

    if user.is_authenticated:
        if user.is_staff:
            orders = Order.objects.all()
        else:
            orders = Order.objects.filter(userid=user)
    else:
        orders = []

    context = {
        'user_is_admin': user.is_staff,
        'orders': orders,
    }

    return render(request, 'RentACar/order_list.html', context)

def order_tracker(request):
    user_is_staff = request.user.is_staff

    if user_is_staff:
        orders = Order.objects.all()
    else:
        orders = Order.objects.filter(userid=request.user)

    context = {
        'user_is_staff': user_is_staff,
        'orders': orders,
    }

    return render(request, 'RentACar/order_tracker.html', context)

def update_order(request):
    if request.method == 'POST' and request.user.is_staff:
        order_number = request.POST.get('orderNumber')
        status = int(request.POST.get('status'))
        
        order = get_object_or_404(Order, orderNumber=order_number)
        order.status = status
        order.save()

        return redirect('order_tracker')
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request method or user is not an admin'})

def check_order_status(request):
    if request.method == 'POST' and request.user.is_authenticated:
        order_number = request.POST.get('orderNumber')

        try:
            order = Order.objects.get(orderNumber=order_number, userid=request.user)
            return JsonResponse({'success': True, 'status': order.get_status_display()})
        except Order.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Order not found for the user'})
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request method or user is not authenticated'})