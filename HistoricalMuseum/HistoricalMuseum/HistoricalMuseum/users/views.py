from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from HistoryMuseum.models import Statistics
from django.contrib.auth.decorators import login_required



def register(request):
    #get forms
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Ο λογαριασμός δημιουργήθηκε για τον χρήστη {username}!')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})

@login_required
def profile(request):
    #get forms
    if request.method == 'POST':
           u_form = UserUpdateForm(request.POST, instance=request.user)
           p_form = ProfileUpdateForm(request.POST,
                                      request.FILES,
                                      instance=request.user.student)
           if u_form.is_valid() and p_form.is_valid():
              user = u_form.save()
              user.refresh_from_db()
              p_form.save()
              messages.success(request, f'Ο λογαριασμός σας ενημερώθηκε!')
              return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.student)
        stats = Statistics.objects.filter(user=request.user)

    
    context = {
                'u_form': u_form,
                'p_form': p_form,
                'stats' : stats,
            }

    return render(request,'users/profile.html', context)
