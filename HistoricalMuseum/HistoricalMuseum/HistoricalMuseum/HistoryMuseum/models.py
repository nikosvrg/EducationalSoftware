from django.db import models
from django.conf import settings
from django.contrib.auth.models import  User
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.core.validators import MaxValueValidator



class Hero(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    context = models.TextField(blank=True)
    hero_img = models.ImageField(upload_to='heroes', default="")


    def __str__(self):
        return self.name


class Test(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    title = models.CharField(max_length=100, null=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='test', on_delete=models.CASCADE)
    
    def __str__(self):
        return f'Test: {self.title}'



class Question(models.Model):
    question = models.TextField(max_length=255)
    test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name='questions')
    hero = models.ForeignKey(Hero, on_delete=models.CASCADE)
    order = models.IntegerField(default=0)
    show = models.BooleanField(default=True)

    class Meta:
        ordering = ['order',]


    def __str__(self):
        return self.question


class Answer(models.Model):
    answer = models.CharField('Answer',max_length=255)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='question_answer')
    correct = models.BooleanField(default=False)


    def __str__(self):
        return f'{self.answer}'


class Statistics(models.Model):
    user = models.ForeignKey(User, on_delete= models.CASCADE)
    test = models.ForeignKey(Test, on_delete=models.CASCADE)

    score = models.PositiveIntegerField(default=0)
    times_read = models.PositiveIntegerField(default=0)
    times_taken = models.PositiveIntegerField(default=0)
    answers_total = models.PositiveIntegerField(default=0)
    answers_correct = models.PositiveIntegerField(default=0)
    answers_wrong = models.PositiveIntegerField(default=0)
    success_rate = models.FloatField(default=0.0)

    passed = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user}, for {self.test}'



