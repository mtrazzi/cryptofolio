from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return HttpResponse("Optimal portfolio: invest everything in bitcoin")

# Create your views here.
