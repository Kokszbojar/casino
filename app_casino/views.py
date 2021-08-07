import random, string

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
    else:
        return render(request, 'base.html')

def coinflip(request):
    if request.user.is_authenticated:
        obj = request.user.gambler
        heads_bet = request.POST.get('heads_bet')
        tails_bet = request.POST.get('tails_bet')
        if (heads_bet == "" or heads_bet == None or int(heads_bet) <= 0) and (tails_bet == "" or tails_bet == None or int(tails_bet) <= 0):
            stuff_for_frontend = {
                'heads_bet': 0,
                'tails_bet': 0,
                'bet_value': 'No flip yet',
                'balance': obj.balance,
            }
            return render(request, 'app_casino/coinflip.html', stuff_for_frontend)
        else:
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
                stuff_for_frontend = {
                    'heads_bet': 0,
                    'tails_bet': 0,
                    'bet_value': 'No flip yet',
                    'balance': obj.balance,
                }
                return render(request, 'app_casino/coinflip.html', stuff_for_frontend)
    
    else:
        return render(request, 'base.html')

def new_message(request):
    if request.user.is_authenticated:
        chatter = request.user.gambler
        message = request.POST.get('message')
        if message != None and message != '':
            letter_id_list = []
            dict = string.printable
            for letter in message:
                letter_id_list.append(pow(string.printable.index(letter), 101, 97))
            message = ''
            for index in letter_id_list:
                message += dict[index]
            models.Message.objects.create(text=message, user=chatter.id)
        return render(request, 'app_casino/api_cipher.html')
    else:
        return render(request, 'base.html')

def read_messages(request):
    if request.user.is_authenticated:
        chatter = request.user.gambler
        encrypted_messages = models.Message.objects.filter(user = chatter.id).values('text')
        dict = string.printable
        messages = []
        for mes in encrypted_messages:
            letter_id_list = []
            dict = string.printable
            for letter in mes['text']:
                letter_id_list.append(pow(string.printable.index(letter), 77, 97))
            message = ''
            for index in letter_id_list:
                message += dict[index]
            messages.append(message)
        stuff_for_frontend = {
            'messages': messages,
        }
        return render(request, 'app_casino/read_messages.html', stuff_for_frontend)
    else:
        return render(request, 'base.html')