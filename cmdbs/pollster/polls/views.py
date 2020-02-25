from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from .models import Questions, Choices
from django.urls import reverse


# Create your views here.
def response(request):
    # return HttpResponse('hello Django! params: {}'.format(style))
    questions = Questions.objects.order_by('create_date')
    return render(request, 'polls/index.html', {'questions': questions})


def detail(request, question_id):
    questions = get_object_or_404(Questions, pk=question_id)
    return render(request, 'polls/detail.html', {'questions': questions})


def results(request, question_id):
    questions = get_object_or_404(Questions, pk=question_id)
    return render(request, 'polls/results.html', {'question': questions})


def votes(request, question_id):
    questions = get_object_or_404(Questions, pk=question_id)
    try:
        selected_choice = questions.choices_set.get(pk=request.POST.get('choice'))
    except (KeyError, Choices.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'questions': questions,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results', args=(questions.id,)))
