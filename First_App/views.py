from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

def index_view(request):
    return render(request, 'index.htm')

def about_view(request):
    return render(request, 'about.htm')

def contact_view(request):
    return render(request, 'contact.htm')