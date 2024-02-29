from django.contrib import messages
from django.shortcuts import render, redirect
from . import models
# Create your views here.
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from .forms import AddRentalForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm
from login_app.models import User
from .models import Comments
from datetime import datetime, timezone


# Rendering home page
def home(request):
    return render(request, 'Home.html')


# Rendering page with filtered vehicles type
def strona1(request, type):
    type_ = str(type)
    items = models.Vehicles_table.objects.filter(group__group__exact=type_)

    context = {'items': items}
    return render(request, 'strona1.html', context)


# Page to show single vehicle
def vehiclePage(request, pk):
    items = models.Vehicles_table.objects.get(id=pk)
    comments = models.Comments.objects.filter(vehicle=items).order_by('-created')

    if request.method == 'POST':
        comm = Comments.objects.create(

            user=request.user,
            vehicle=items,
            text=request.POST.get('body'),
        )

        return redirect('VehiclePage', pk=items.id)

    context = {'items': items, 'comments': comments}
    return render(request, 'VehiclePage.html', context)


# Page to creating listing
@login_required(login_url='loginpage')
def createRental(request):
    form = AddRentalForm()
    if request.method == "POST":

        form = AddRentalForm(request.POST)
        if form.is_valid():
            vehicle = form.save(commit=False)
            vehicle.owner = request.user
            vehicle.save()
            messages.success(request, "You've successfuly created listing", extra_tags='success')
            return redirect('Home')
    else:
        form = AddRentalForm()

    context = {'form': form}

    return render(request, 'add_rental/create_rental.html', context)


# Page to updating listing
@login_required(login_url='loginpage')
def updateRental(request, pk):
    vehicle = models.Vehicles_table.objects.get(id=pk)
    form = AddRentalForm(instance=vehicle)

    if request.user != vehicle.owner:
        return HttpResponse("You cant be here")

    if request.method == 'POST':
        form = AddRentalForm(request.POST, instance=vehicle)
        if form.is_valid():
            form.save()
            messages.success(request, "You've successfuly updated listing", extra_tags='success')
            return redirect('Home')
    context = {'form': form}
    return render(request, 'add_rental/create_rental.html', context)


# Page to deleting rental listing
@login_required(login_url='loginpage')
def deleteRental(request, pk):
    vehicle = models.Vehicles_table.objects.get(id=pk)
    if request.user != vehicle.owner:
        return HttpResponse("You cant be here")

    if request.method == 'POST':
        vehicle.delete()
        messages.success(request, "You've successfuly deleted listing", extra_tags='success')
        return redirect('Home')

    return render(request, 'delete.html', {'obj': vehicle})


# Start renting vehicle
@login_required(login_url='loginpage')
def startRenting(request, pk):
    vehicle = models.Vehicles_table.objects.get(id=pk)

    if request.user == vehicle.owner:
        return HttpResponse("You cant be here - you can't rent your own vehicle :/")

    if request.method == 'POST':
        if vehicle.is_rented:
            return HttpResponse("Vehicle is currently rented :/")
        else:
            vehicle.is_rented = True
            vehicle.currently_rented_by = request.user
            vehicle.rent_start = datetime.now(timezone.utc)
            # price = vehicle.price
            # user_renting = request.user
            # user_renting.spending += price
            # vehicle.owner.earning += price
            vehicle.save()
            messages.success(request, "You've successfuly rented vehicle", extra_tags='success')
        return redirect('Home')

    return render(request, 'conf_rent.html', {'obj': vehicle})


def index(request):
    comments = Comments.objects.all()
    return render(request, 'index.html', {'comments': comments})


# Add comment
@login_required
def add_comment(request):
    if request.method == 'POST':
        text = request.POST.get('text')
        if text:
            Comments.objects.create(user=request.user, text=text)
            return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'})


# Deleting comment
@login_required(login_url='loginpage')
def delete_comment(request, pk):
    comment = Comments.objects.get(id=pk)

    if request.user != comment.user:
        return HttpResponse('You shouldnt be here!')

    if request.method == 'POST':
        comment.delete()
        messages.success(request, "You've successfuly deleted comment", extra_tags='success')
        return redirect('Home')

    return render(request, 'delete.html', {'object': comment})


# Creating user profile
def UserProfile(request):
    user = request.user
    vehicles = models.Vehicles_table.objects.filter(owner=user)
    rented_vehicles = models.Vehicles_table.objects.filter(currently_rented_by=user)

    return render(request, 'UserProfile.html', {'user': user, 'vehicles': vehicles, 'rented_vehicles': rented_vehicles})


# Stop renting vehicle
@login_required(login_url='loginpage')
def stopRenting(request, pk):
    vehicle = models.Vehicles_table.objects.get(id=pk)
    user_renting = vehicle.currently_rented_by
    owner = vehicle.owner

    if request.user == vehicle.owner:
        return HttpResponse("You cant be here :/")

    if request.user != user_renting:
        return HttpResponse("You cant be here! You dont rent it!")

    if request.method == 'POST':
        if not vehicle.is_rented:
            return HttpResponse("Vehicle is not currently rented :/")
        else:
            now = datetime.now(timezone.utc)
            price = vehicle.price * ((now - vehicle.rent_start).days + 1)
            vehicle.is_rented = False
            vehicle.currently_rented_by = None
            vehicle.rent_start = None

            user_renting.spending = user_renting.spending + price

            owner.earning = owner.earning + price

            user_renting.save()
            vehicle.save()
            owner.save()
            messages.success(request, "You've successfuly stopped renting vehicle", extra_tags='success')

        return redirect('Home')

    return render(request, 'conf_rent.html', {'obj': vehicle})
