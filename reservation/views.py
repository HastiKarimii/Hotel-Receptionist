from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views.generic.edit import *
from django.urls import reverse_lazy
from django.contrib import messages
from django.views.generic import *
from django.db.models import Q
from .models import *
from .forms import *


class ReservationCreateView(LoginRequiredMixin, CreateView):
    template_name = "CreateReservation.html"
    form_class = ReservationForm
    success_url = reverse_lazy('listreserve')

    def form_valid(self, form):
        return super(ReservationCreateView, self).form_valid(form)


class ReservationUpdateView(LoginRequiredMixin, UpdateView):
    model = Reservation
    template_name = "UpdateReservation.html"
    success_url = reverse_lazy('listreserve')
    form_class = ReservationForm

    def form_valid(self, form):
        self.object = form.save()
        messages.success(self.request, 'The Resarvation information Edited successfully!')
        return super().form_valid(form)

    def get_initial(self, *args, **kwargs):
        initials = super(ReservationUpdateView, self).get_initial(**kwargs)
        return initials


class ReservationListView(LoginRequiredMixin, ListView):
    model = Reservation
    template_name = 'ListReservation.html'
    fields = "__all__"

    def get_queryset(self):
        query = self.request.GET.get('name', '')
        if query:
            object_list = self.model.objects.filter(
                Q(first_name__istartswith=query) |
                Q(last_name__istartswith=query) |
                Q(phone_number__iexact=query) |
                Q(id__iexact=query) |
                Q(login_date__iexact=query) |
                Q(logout_date__iexact=query)
            )
        else:
            object_list = self.model.objects.all()
        return object_list


class ReservationDeleteView(LoginRequiredMixin, DeleteView):
    model = Reservation
    # context_object_name = 'reserve'
    success_url = reverse_lazy('listreserve')
    template_name = 'DeleteReservation.html'

    def form_valid(self, form):
        messages.success(self.request, "The task was deleted successfully.")
        return super(ReservationDeleteView, self).form_valid(form)

    #### it is used for script confirmation of delete
    # def post(self, request, *args, **kwargs):
    #     messages.success(self.request, 'Deleting this Reservation was successfully')
    #     return self.delete(self.request, *args, **kwargs)

    # ### it is used for a tag in template
    # def get(self, *a, **kw):
    #     messages.success(self.request, 'Deleting this Reservation was successfully')
    #     return self.delete(*a, **kw)
