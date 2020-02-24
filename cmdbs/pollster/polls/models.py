from django.db import models
from django.utils import timezone
import datetime


# Create your models here.
# noinspection PyTypeChecker
class Questions(models.Model):

    question_text = models.CharField(max_length=200)
    create_date = models.DateTimeField('date published')

    def __str__(self):
        return self.question_text

    def was_published_recently(self):
        return self.create_date >= timezone.now() - datetime.timedelta(days=1)


class Choices(models.Model):

    questions = models.ForeignKey(Questions, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text


# Questions.object.create(field01="", field02="")   创建数据
# question = Questions.object.get(pk=1)             查询主键获取整条数据
# question.update(field="")                         更改数据
# question.delete()                                 删除数据
