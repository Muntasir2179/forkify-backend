from django.shortcuts import render
from django.views.generic import TemplateView

# define your views here

class Index(TemplateView):
    template_name = 'recipe/index.html'    
