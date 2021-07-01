from django.shortcuts import (render, get_object_or_404, redirect)
from django.views.generic import UpdateView, CreateView, ListView, DeleteView, DetailView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import permission_required, login_required
from django.urls import reverse_lazy
from django.urls import reverse
from datetime import date
from datetime import timedelta
from datetime import datetime
import locale

from .forms import TransactionForm
from products.forms import (ProductForm, ProductForm_tmp)
from products.models import (Product, Product_tmp)
from .models import Transaction
# Create your views here.

class TransactionCalendarView(LoginRequiredMixin, ListView):
    #queryset = Transaction.objects.all()
    template_name = 'transaction/calendar.html'

    def get_transaction_detail(self, date):
        transaction_list = Transaction.objects.filter(delivery_date=date)
        transaction_number = 0
        total_price = 0
        for transaction in transaction_list:
            product_list = transaction.product_set.all()
            total_price = transaction.delivery_fee
            transaction_number = transaction_number +1
            for product in product_list:
                total_price = total_price + product.quantity *  product.price

        tuple = [transaction_number, total_price]

        return tuple

    def get(self, request, *args, **kwargs):

        locale.setlocale(locale.LC_ALL, 'French')

        today = date.today()
        #find monday
        start_date = today - timedelta(days= today.weekday())
        #plot 4 weeks
        end_date = today +  timedelta(days= 34)

        week_list = []
        day_list = [start_date]
        day_list_str = [start_date.strftime('%d %B')]
        tuple = self.get_transaction_detail(start_date)
        price_list = [tuple[1]]
        number_list = [tuple[0]]
        while start_date <= end_date:
            start_date = start_date + timedelta(days=1)
            day_list.extend([start_date])
            day_list_str.extend([start_date.strftime('%d %B')])
            tuple = self.get_transaction_detail(start_date)
            price_list.extend([tuple[1]])
            number_list.extend([tuple[0]])
            if start_date.weekday() == 6:
                day_transaction_list = zip(day_list,day_list_str, price_list, number_list)
                week_list.extend([day_transaction_list])
                day_list = []
                day_list_str = []
                price_list = []
                number_list = []
        context = {}
        context['week_list'] = week_list
        context['today'] = date.today()
        return render(request, self.template_name,context)


class TransactionDeleteProduct(LoginRequiredMixin, DeleteView):
    model = Product_tmp
    queryset = Product_tmp.objects.all()
    template_name = 'transaction/create.html'

    def get(self, request, *args, **kwargs):
        id = self.kwargs.get('pk')
        if request.GET.get("next",'') != 'None':
                url = '/transaction/create/' + request.GET.get("next",'') + '/'
        else:
                url = '/transaction/create/'
        product = self.get_object()
        product.delete()
        return redirect(url)

    def get_object(self):
        id = self.kwargs.get('pk')
        obj = None
        if id is not None:
            obj = get_object_or_404(Product_tmp, id=id)
        return obj

class TransactionDeleteAllProduct(LoginRequiredMixin, DeleteView):
    model = Product_tmp
    queryset = Product_tmp.objects.all()
    template_name = 'transaction/create.html'

    def get(self, request, *args, **kwargs):
        id = self.kwargs.get('pk')
        if request.GET.get("next",'') != 'None':
                url = '/transaction/create/' + request.GET.get("next",'') + '/'
        else:
                url = '/transaction/create/'
        for product_tmp in self.get_queryset():
            product_tmp.delete()
        return redirect(url)

class TransactionCreateView(LoginRequiredMixin, View):
    model = Product_tmp
    queryset = Product_tmp.objects.all()
    template_name = 'transaction/create.html'

    def get_sum_price(self):
        sum = 0
        for product_tmp in self.get_queryset():
            sum = sum + product_tmp.price * product_tmp.quantity
        return sum

    def get_object(self):
        id = self.kwargs.get('pk')
        obj = None
        if id is not None:
            obj = get_object_or_404(Product_tmp, id=id)
        return obj

    def get_success_url(self):
        current_url = self.request.get_full_path()
        if current_url=='/client/list/create/':
            return reverse('client_list')
        else:
            return reverse('transaction_list')

    def get_queryset(self):
        return Product_tmp.objects.all()

    def get(self, request, *args, **kwargs):
        context = {}
        id = self.kwargs.get('pk')

        context['product_form'] = ProductForm_tmp()
        if id is not None:
            transaction_form = TransactionForm(initial={'client': id})
        else:
            transaction_form = TransactionForm()
        context['transaction_form'] = transaction_form
        context['product_list'] = self.get_queryset()
        context['price_sum'] = self.get_sum_price()
        return render(request, self.template_name,context)


    def post(self, request, *args, **kwargs):

        if 'pk' in kwargs:
            transaction_form = TransactionForm(initial={'client': kwargs['pk']})
        else:
            transaction_form = TransactionForm()

        #case where we save a product
        if request.POST.get("product"):
            productForm = ProductForm_tmp(request.POST)
            if productForm.is_valid():
                product = productForm.save()
            context = {}
            context['product_form'] = ProductForm_tmp()
            context['transaction_form'] = transaction_form
            context['product_list'] = self.get_queryset()
            context['price_sum'] = self.get_sum_price()
            return render(request, self.template_name ,context)

        elif request.POST.get("delete"):
            context = {}
            product = self.get_object()
            if product is not None:
                product.delete()
                context['product_list'] = self.get_queryset()
                context['product_form'] = ProductForm_tmp()
                context['transaction_form'] = TransactionForm()
                context['price_sum'] = self.get_sum_price()
            return render(request, self.template_name ,context)
        else:
            transactionForm = TransactionForm(request.POST)
            if transactionForm.is_valid():
                transaction = transactionForm.save()
                for product_tmp in self.get_queryset():
                    product =  Product.objects.create(designation=product_tmp.designation, quantity=product_tmp.quantity,price=product_tmp.price,transaction=transaction)
                    product_tmp.delete()
            context = {}
            context['product_form'] = ProductForm_tmp()
            context['transaction_form'] = TransactionForm()
            context['product_list'] = self.get_queryset()
            context['price_sum'] = self.get_sum_price()
            return redirect('transaction_detail', transaction.id)

            return render(request, self.template_name ,context)

class TransactionDetailView(LoginRequiredMixin, DetailView):
    model = Transaction
    template_name = 'transaction/detail.html'

    def get_transaction(self):
        id = self.kwargs.get('pk')
        Transaction = None
        if id is not None:
            transaction = get_object_or_404(self.model, id=id)
        return transaction

    def get(self, request, *args, **kwargs):
        context = {}
        transaction = self.get_transaction()
        product_list= transaction.product_set.all()
        total_price = 0
        for product in product_list:
            total_price = total_price + product.price * product.quantity
        context['transaction'] = transaction
        context['product_list'] = product_list
        context['total_price'] = total_price
        return render(request, self.template_name, context)


class TransactionDeleteView(LoginRequiredMixin, DeleteView):
    template_name = 'transaction/delete.html'
    queryset = Transaction.objects.all()

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
        transaction = self.get_object()
        context['form'] = transaction
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
                url = 'transaction_list'
                return reverse(url)

class TransactionDayView(LoginRequiredMixin, ListView):
    queryset = Transaction.objects.all()
    template_name = 'transaction/day.html'

    def get_sum_price(self):
        sum = 0
        for product_tmp in self.get_queryset():
            sum = sum + product.price * product.quantity
        return sum

    def get(self, request, *args, **kwargs):
        context = {}
        transaction_list = Transaction.objects.filter(delivery_date=kwargs['date'])
        transaction_price = list()
        for transaction in transaction_list:
            product_list =  transaction.product_set.all()
            transaction_price_tmp = transaction.delivery_fee
            for product in product_list:
                transaction_price_tmp = transaction_price_tmp + product.price * product.quantity
            transaction_price.extend([transaction_price_tmp])
        mylist = zip(transaction_list, transaction_price)
        context['mylist'] = mylist
        date = datetime.strptime(kwargs['date'],'%Y-%m-%d')
        context['day'] = date.date()
        return render(request, self.template_name,context)

class TransactionListView(LoginRequiredMixin, ListView):
    queryset = Transaction.objects.all()
    template_name = 'transaction/list.html'

    def get_sum_price(self):
        sum = 0
        for product_tmp in self.get_queryset():
            sum = sum + product.price * product.quantity
        return sum

    def get(self, request, *args, **kwargs):
        context = {}
        transaction_list = Transaction.objects.all()
        transaction_price = list()
        for transaction in transaction_list:
            product_list =  transaction.product_set.all()
            transaction_price_tmp = transaction.delivery_fee
            for product in product_list:
                transaction_price_tmp = transaction_price_tmp + product.price * product.quantity
            transaction_price.extend([transaction_price_tmp])
        mylist = zip(transaction_list, transaction_price)
        context['mylist'] = mylist
        return render(request, self.template_name,context)

class TransactionEditView(LoginRequiredMixin, UpdateView):
    queryset = Transaction.objects.all()
    template_name = 'transaction/edit.html'
    form_class = TransactionForm

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
        transaction = self.get_object()
        context['form'] = TransactionForm(instance=transaction)
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
                url = 'transaction_list'
                return reverse(url)

    def get_object(self):
        id_=self.kwargs.get('pk')
        return(get_object_or_404(Transaction,id=id_))
