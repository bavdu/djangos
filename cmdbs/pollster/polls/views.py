from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404
from .models import Questions


# Create your views here.
def response(request):
    # return HttpResponse('hello Django! params: {}'.format(style))
    questions = Questions.objects.order_by('create_date')
    return render(request, 'polls/index.html', {'questions': questions})


def detail(request, questions_id):
    questions = get_object_or_404(Questions, pk=questions_id)
    return render(request, 'polls/detail.html', {'questions': questions})


def results(request, questions_id):
    return HttpResponse('you are looking at result of questions: {}'.format(questions_id))


def votes(request, questions_id):
    return HttpResponse('you are looking at votes: {}'.format(questions_id))
