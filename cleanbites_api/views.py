from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def get_places(request):
    return HttpResponse('ok')
