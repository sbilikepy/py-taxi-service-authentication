from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views import generic

from .forms import CarForm
from .models import Driver, Car, Manufacturer


@login_required
def index(request):
    num_drivers = Driver.objects.count()
    num_cars = Car.objects.count()
    num_manufacturers = Manufacturer.objects.count()

    num_visits = request.session.get("num_visits", 0) + 1
    request.session["num_visits"] = num_visits

    context = {
        "num_drivers": num_drivers,
        "num_cars": num_cars,
        "num_manufacturers": num_manufacturers,
        "num_visits": num_visits,
    }

    return render(request, "taxi/index.html", context=context)


class ManufacturerListView(LoginRequiredMixin, generic.ListView):
    model = Manufacturer
    context_object_name = "manufacturer_list"
    template_name = "taxi/manufacturer_list.html"
    paginate_by = 5


class CarListView(LoginRequiredMixin, generic.ListView):
    model = Car
    paginate_by = 50
    queryset = Car.objects.select_related("manufacturer")


class CarDetailView(LoginRequiredMixin, generic.DetailView):
    model = Car


def car_create_view(request: HttpRequest) -> HttpResponse:  # bad practice
    context = {}
    form = CarForm(request.POST or None)
    if form.is_valid():
        # new_car = Car.objects.create(
        #     model=form.cleaned_data["model"],
        #     manufacturer=Manufacturer.objects.get(
        #         pk=int(form.cleaned_data["manufacturer_id"]))
        # )
        form.save()

        return HttpResponseRedirect(reverse("taxi:car-list"))
    context["form"] = form
    return render(request, "taxi/car_form.html", context=context)
    # if request.method == "GET":
    #     context = {
    #         "form": CarForm()
    #     }
    #     return render(request, template_name="taxi/car_form.html",
    #                   context=context)
    #
    # if request.method == "POST":
    #     form = CarForm(request.POST)
    #     if form.is_valid():
    #         new_car = Car.objects.create(
    #             model=form.cleaned_data["model"],
    #             manufacturer=Manufacturer.objects.get(
    #                 pk=int(form.cleaned_data["manufacturer_id"]))
    #         )
    #         new_car.save()
    #         return HttpResponseRedirect(reverse("taxi:car-list"))
    #
    #     context = {
    #         "form": form
    #     }
    #
    #     return render(request, "taxi/car_form.html", context=context)


class DriverListView(LoginRequiredMixin, generic.ListView):
    model = Driver
    paginate_by = 5


class DriverDetailView(LoginRequiredMixin, generic.DetailView):
    model = Driver
    queryset = Driver.objects.prefetch_related("cars__manufacturer")
