from django.db import models
import datetime


# Create your models here.
class Question(models.Model):

    questions_text = models.CharField(max_length=200, blank=True)
    date = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return self.questions_text


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200, blank=True)
    votes = models.IntegerField(default=0, blank=True)

