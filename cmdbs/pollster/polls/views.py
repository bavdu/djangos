from django.shortcuts import render
from django.http import HttpResponse
from .models import Questions


# Create your views here.
def response(request):
    # return HttpResponse('hello Django! params: {}'.format(style))
    questions = Questions.objects.order_by('create_date')
    return HttpResponse(', '.join([question.question_text for question in questions]))


def detail(request, questions_id):
    return HttpResponse('you are looking at question {}'.format(questions_id))


def results(request, questions_id):
    return HttpResponse('you are looking at result of questions: {}'.format(questions_id))


def votes(request, questions_id):
    return HttpResponse('you are looking at votes: {}'.format(questions_id))
