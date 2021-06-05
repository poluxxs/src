from django.shortcuts import (render, get_object_or_404, redirect)
from django.views.generic import UpdateView, CreateView, ListView, DeleteView, DetailView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import permission_required, login_required

from django.views.generic.list import MultipleObjectMixin

from django.http import HttpResponse, HttpResponseRedirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.urls import reverse

from .forms import ClientForm
from .models import Client

class ClientListView(LoginRequiredMixin, ListView):
    template_name = 'client/list.html'
    queryset = Client.objects.all()

class ClientUpdateView(LoginRequiredMixin, UpdateView):
    form_class = ClientForm
    template_name = 'client/edit.html'
    success_url = reverse_lazy('client_list')

    def get_object(self):
        id_=self.kwargs.get('pk')
        return(get_object_or_404(Client,id=id_))

    def get(self, request, *args, **kwargs):
        if request.GET.get("next",'') != '':
                url =  request.GET.get("next",'')
                url =  'next=' + url
        elif request.GET.get("nextID",'') != '':
                url =  request.GET.get("nextID",'')
                url =  'nextID=' + url
        else:
                url = 'next=urltransaction_list'
        context = {}
        context['next_url'] = url
        client = self.get_object()
        context['form'] = ClientForm(instance=client)
        return render(request, self.template_name, context)

    def get_success_url(self):
        if self.request.GET.get("next",'') != '':
                url =  self.request.GET.get("next",'')
                return reverse(url)
        elif self.request.GET.get("nextID",'') != '':
                url =  self.request.GET.get("nextID",'')
                pk =  url[(len(url)-1):len(url)]
                url =  url[0:len(url)-1]
                return reverse(url, kwargs={'pk': pk})
        else:
                url = 'client_list'
                return reverse(url)

class ClientCreateView(LoginRequiredMixin, CreateView):
    model = Client
    form_class = ClientForm
    template_name = 'client/create.html'
    queryset = Client.objects.all()

    def form_valid(self, form):
        print(form.cleaned_data)
        return super().form_valid(form)

    def get_success_url(self, **kwargs):
        print(kwargs)
        print(self.kwargs.get('pk'))

        if self.kwargs.get('pk') == 0:
            return reverse('client_list')
        else:
            return reverse('transaction_create', kwargs={'pk': self.object.id})

class ClientDeleteView(LoginRequiredMixin, DeleteView):
    model = Client
    template_name = 'client/delete.html'
    success_url = reverse_lazy('client_list')
    queryset = Client.objects.all()


class ClientDetailView(LoginRequiredMixin, DetailView):
    model = Client
    template_name = 'client/detail.html'

    def get_client(self):
        id = self.kwargs.get('pk')
        client = None
        if id is not None:
            client = get_object_or_404(Client, id=id)
        return client

    def get(self, request, *args, **kwargs):
        context = {}
        client = self.get_client()
        transaction_list= client.transaction_set.all()
        total_price = 0
        transaction_price = list()
        for transaction in transaction_list:
            product_list =  transaction.product_set.all()
            transaction_price_tmp = transaction.delivery_fee
            total_price = total_price +  transaction.delivery_fee
            for product in product_list:
                total_price = total_price + product.price * product.quantity
                transaction_price_tmp = transaction_price_tmp + product.price * product.quantity
            transaction_price.extend([transaction_price_tmp])
        mylist = zip(transaction_list, transaction_price)
        context['mylist'] = mylist
        context['client'] = client
        context['total_price'] = total_price
        return render(request, self.template_name,context)
