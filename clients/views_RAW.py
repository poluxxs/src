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

class ClientListView(LoginRequiredMixin, View):
    template_name = 'client/list.html'
    queryset = Client.objects.all()

    def get_queryset(self):
        return self.queryset

    def get(self, request, *args,**kwargs):
        context = {}
        form = ClientForm()
        context['form'] = form
        context['object_list'] = self.get_queryset()
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        context = {}
        form = ClientForm(request.POST)
        if form.is_valid():
            form.save()
        context['object_list'] = self.get_queryset()
        context['form'] = form
        return render(request, self.template_name ,context)


class ClientUpdateView(UpdateView):
    model = Client
    form_class = ClientForm
    template_name = 'client/edit.html'
    success_url = reverse_lazy('client_list')

    def get_object(self):
        id = self.kwargs.get('pk')
        obj = None
        if id is not None:
            obj = get_object_or_404(Client, id=id)
        return obj

    def get(self, request, id=None, *args, **kwargs):
        context = {}
        obj = self.get_object()
        if obj is not None:
            form = ClientForm(instance =obj)
            context['object'] = obj
            context['form'] = form
        return render(request, self.template_name,context)

    def post(self, request, id=None, *args, **kwargs):
        context = {}
        obj = self.get_object()
        if obj is not None:
            form = ClientForm(request.POST, instance = obj)
            if form.is_valid():
                form.save()
            context['object'] = obj
            context['form'] = form
        return render(request, 'client/list.html',context)

class ClientCreateView(CreateView):
    model = Client
    form_class = ClientForm
    template_name = 'client/create.html'

    def get_success_url(self):
        current_url = self.request.get_full_path()
        if current_url=='/client/list/create/':
            return reverse('client_list')
        else:
            return reverse('transaction_list')

    def get(self, request, *args, **kwargs):
        form = ClientForm()
        context = {"form":form}
        return render(request, self.template_name,context)

    #def post(self, request, *args, **kwargs):
        #form = ClientForm(request.POST)
        #if form.is_valid():
            #form.save()
        #context = {"form":form}
        #return render(request, reverse(self.get_success_url()) ,context)

class ClientDeleteView(DeleteView):
    model = Client
    template_name = 'client/delete.html'
    success_message = 'Success: client was created.'
    def get_succes_url(self):
        return reverse('client_list')

    def get_object(self):
        id = self.kwargs.get('pk')
        obj = None
        if id is not None:
            obj = get_object_or_404(Client, id=id)
        return obj

    def get(self, request, id=None, *args, **kwargs):
        context = {}
        obj = self.get_object()
        if obj is not None:
            context['object'] = obj
        return render(request, self.template_name,context)

    def post(self, request, id=None, *args, **kwargs):
        context = {}
        obj = self.get_object()
        if obj is not None:
            obj.delete()
            context['object'] = None
            return redirect('/client/list/')
        return render(request, self.template_name ,context)


class ClientDetailView(DetailView):
    model = Client
    form_class = ClientForm
    template_name = 'client/delete.html'
    success_message = 'Success: client was created.'

    def get_succes_url(self):
        return reverse('client_list')
