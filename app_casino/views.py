import random

from django.shortcuts import render
from . import models

from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic

# Create your views here.
def home(request):
    return render(request, 'base.html')

class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'

def update_balance(request):
    if request.user.is_authenticated:
        obj = request.user.gambler
        obj.balance += 100
        obj.save()
        return render(request, 'base.html')

def coinflip(request):
    if request.user.is_authenticated:
        obj = request.user.gambler
        heads_bet = request.POST.get('heads_bet')
        tails_bet = request.POST.get('tails_bet')
        if heads_bet == "" or heads_bet == None: 
            heads_bet = 0
            if tails_bet == "" or tails_bet == None:
                tails_bet = 0
        elif tails_bet == "" or tails_bet == None:
            tails_bet = 0
        if int(heads_bet) + int(tails_bet) <= obj.balance:
            models.CoinBet.objects.create(heads_bet=heads_bet, tails_bet=tails_bet)
            flip = random.randint(0, 1)
            if flip == 0:
                obj.balance += int(heads_bet)
                obj.balance -= int(tails_bet)
                flip = "heads"
            else:
                obj.balance -= int(heads_bet)
                obj.balance += int(tails_bet)
                flip = "tails"
            obj.save()

            stuff_for_frontend = {
                'heads_bet': int(heads_bet),
                'tails_bet': int(tails_bet),
                'bet_value': flip,
                'balance': obj.balance,
            }

            return render(request, 'app_casino/coinflip.html', stuff_for_frontend)

        else:
            return render(request, 'app_casino/coinflip.html')
    
    else:
        return render(request, 'base.html')