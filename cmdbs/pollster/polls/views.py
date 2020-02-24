from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.
def response(request, style):
    return HttpResponse('hello Django! params: {}'.format(style))
