from django.shortcuts import render
from django.shortcuts import (render, get_object_or_404, redirect)
from django.views.generic import UpdateView, CreateView, ListView, DeleteView, DetailView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import permission_required, login_required
from django.urls import reverse_lazy
from django.urls import reverse

from .forms import ProductForm
from .forms import ProductForm_tmp
from .models import Product_tmp
from .models import Product

from transactions.models import Transaction

# Create your views here.
class ProductDeleteView(LoginRequiredMixin, DeleteView):
    template_name = 'transaction/detail.html'
    queryset = Product.objects.all()

    def get_product(self):
        id = self.kwargs.get('pk')
        product = None
        if id is not None:
            product = get_object_or_404(Product, id=id)
        return product

    def get(self, request, *args, **kwargs):
        product = self.get_product()
        product.delete()

        if request.GET.get("next",'') != '':
                url =  request.GET.get("next",'')
                return redirect(url)
        elif request.GET.get("nextID",'') != '':
                url =  request.GET.get("nextID",'')
                pk =  url[(len(url)-1):len(url)]
                url =  url[0:len(url)-1]
                return redirect(url,int(pk))
        else:
                url = 'transaction_list'
                return redirect(url)


class ProductCreateView(LoginRequiredMixin, CreateView):
    template_name = 'product/create.html'
    form_class = ProductForm
    mopdel = Product
    queryset = Product.objects.all()

    def post(self, request, *args, **kwargs):
        productForm_tmp = ProductForm_tmp(request.POST)
        product_tmp = productForm_tmp.save(commit=False)
        transaction = get_object_or_404(Transaction,id=kwargs['pk'])
        product =  Product.objects.create(designation=product_tmp.designation, quantity=product_tmp.quantity,price=product_tmp.price,transaction=transaction)
        product.save()
        return self.get_success_url()

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
        product = self.get_object()
        context['form'] = ProductForm()
        return render(request, self.template_name, context)

    def get_success_url(self):
        if self.request.GET.get("next",'') != '':
                url =  self.request.GET.get("next",'')
                return redirect(url)
        elif self.request.GET.get("nextID",'') != '':
                url =  self.request.GET.get("nextID",'')
                pk =  url[(len(url)-1):len(url)]
                url =  url[0:len(url)-1]
                return redirect(url,int(pk))
        else:
                url = 'index'
                return redirect(url)

class ProductEditView(LoginRequiredMixin, UpdateView):
    queryset = Product.objects.all()
    template_name = 'product/edit.html'
    form_class = ProductForm

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
        product = self.get_object()
        context['form'] = ProductForm(instance=product)
        return render(request, self.template_name, context)

    def get_success_url(self):
        print('je suis la')
        if self.request.GET.get("next",'') != '':
                url =  self.request.GET.get("next",'')
                return reverse(url)
        elif self.request.GET.get("nextID",'') != '':
                url =  self.request.GET.get("nextID",'')
                pk =  url[(len(url)-1):len(url)]
                url =  url[0:len(url)-1]
                return reverse(url, kwargs={'pk': pk})
        else:
                url = 'index'
                return reverse(url)

    def get_object(self):
        id_=self.kwargs.get('pk')
        return(get_object_or_404(Product,id=id_))
