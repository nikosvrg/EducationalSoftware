from django import forms
from .models import *
from django.db import models
from django.contrib.auth.models import User



class HeroForm(forms.ModelForm):
    class Meta:
        model = Hero
        fields = ['id', 'name', 'hero_img', 'context', 'description']



class TestForm(forms.Form):

    limit= 0 
    user = None

    def __init__(self, *args, **kwargs):
        hero = kwargs.pop('hero')
        self.limit = kwargs.pop('limit')
        super(TestForm, self).__init__(*args, **kwargs)

        #get test for current hero  
        self.test = Test.objects.get(id=hero)

        self.questions = self.test.questions.filter(show=True)

        if self.limit < len(self.questions):
            self.questions = self.questions[:self.limit]

        widget = forms.Select(attrs={'class': 'browser-default'})

        #create question for number of limit
        for counter, q in enumerate(self.questions):
            self.fields[f'question{counter}'] = forms.ModelChoiceField(label=q,
                                                                          queryset=Answer.objects.filter(question=q,
                                                                                                         question__test=self.test),
                                                                                                         required=True,
                                                                                                         empty_label=None,
                                                                                                         widget=widget )
