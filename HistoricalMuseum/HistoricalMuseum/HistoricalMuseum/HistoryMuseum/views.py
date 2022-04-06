from django.views.generic import TemplateView
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse, request, Http404
from django.views.generic.edit import FormView
from django.forms import formset_factory
from .forms import *
from .models import *


def homepage(request):
    context = {

        }
    return render(request, 'HistoryMuseum/homepage.html', context)





class HeroPageView(LoginRequiredMixin,TemplateView):

    def get(self,request, *args, **kwargs):
        user = request.user

        heroes = Hero.objects.all()
        context = {
            'heroes': heroes
        }

        return render(request, 'HistoryMuseum/hero.html', context)



class HeroRedirectView(LoginRequiredMixin, TemplateView):

    def get(self, request, *args, **kwargs):
        user = request.user

        return redirect(f'/hero/{user.student.test_taking}/')

class TheoryPageView(LoginRequiredMixin,TemplateView):
    template_name = 'HistoryMuseum/theory.html'

    def get(self, request, hero_id, *args, **kwargs):
        user = request.user

        try:
            hero_theory = Hero.objects.filter(id=hero_id)
        except:
            raise Http404('Hero does not exit')

        if hero_id is None:
            hero_id = user.student.hero_studying

        try:
            t = Test.objects.get(id=hero_id)
            stats, created = Statistics.objects.get_or_create(user=user, test=t)
        except:
            raise Htpp404('Hero should be followed by Test')
        
        stats.times_read += 1
        stats.save()
        context = {
            'hero_theory': hero_theory,
            'hero_id': hero_id
            
        }

        return render(request, self.template_name, context)



class TestRedirectView(LoginRequiredMixin, TemplateView):
    def get(self, request, *args, **kwargs):
        user = request.user
        return redirect('f/hero/test/{user.student.test_taking}/')

class TestPageView(LoginRequiredMixin, TemplateView):
    template_name = 'HistoryMuseum/test.html'

    def get(self, request, id, *args, **kwargs):
        user = request.user

        if id is None:
            id = user.student.hero_studying

        # if id > user.student.hero_studying:
        #     return redirect(f'/hero/test/{user.student.test_taking}/')

        try:
            t = Test.objects.get(id=id)

        except:
            return Http404()

        #count questions
        limit = Question.objects.filter(test=t, show=True).count()

        form = TestForm(hero=id, limit=limit)

        context = {
            'form' : form,
            'test': t
        }

        return render(request, self.template_name, context)

    def post(self, request, id, *args, **kwargs):
        user = request.user
        t = Test.objects.get(id=id)
        limit = Question.objects.filter(test=t, show=True).count()
        form = TestForm(request.POST, hero=id, limit=limit)

        if form.is_valid():
            
            stats, created = Statistics.objects.get_or_create(user=user, test=t)
            data = form.cleaned_data

            current_correct_answers = 0

            for i in range(limit):

                user_answer = data.get(f'question{i}')

                if user_answer.correct:
                    current_correct_answers += 1

            stats.answers_correct += current_correct_answers
            stats.answers_wrong += limit - current_correct_answers
            stats.answers_total += limit

            stats.times_taken +=1
            stats.success_rate = round(stats.answers_correct / stats.answers_total, 2 )*100
            stats.score = round(current_correct_answers / limit, 2) * 100
            #score > 60% passed
            if current_correct_answers / limit >= 0.6:
                stats.passed = True

            else:
                stats.passed = False
                user.save()
                stats.save()
                return redirect(f'/hero/not_passed')
             
            user.save()
            stats.save()
            return redirect(f'/hero/passed')


        context = {
            'form': form,
            'test': t,
            'stats': stats,
        }

        return render(request, self.template_name, context)






class PassedView(LoginRequiredMixin, TemplateView):

    template_name = 'HistoryMuseum/passed.html'

    def get(self, request, *args, **kwargs):
        user = request.user
        stats = Statistics.objects.filter(user=request.user)
        # try:
        #     test = Test.objects.filter(id=test_id)
        # except:
        #     raise Http404('Test does not exit')
        context = {
            'stats' : stats
        }

        return render(request, self.template_name, context)


class NotPassedView(LoginRequiredMixin, TemplateView):

    template_name = 'HistoryMuseum/not_passed.html'
    def get(self, request , *args, **kwargs):
        user = request.user
        # try:
        #     test = Test.objects.filter(id=test_id)
        # except:
        #     raise Http404('Test does not exit')
        stats = Statistics.objects.filter(user=request.user)
        context = {
            'stats' : stats,
     
        }

        return render(request, self.template_name, context)
