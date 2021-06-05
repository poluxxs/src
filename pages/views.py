from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import UpdateView, CreateView, ListView, DeleteView, DetailView, View, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.

class IndexView(LoginRequiredMixin, TemplateView):
    template_name = "index.html"
