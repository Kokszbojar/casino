from django.db import models
from django.contrib.auth.models import User
from django.db.models.fields import CharField, IntegerField
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class Gambler(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.IntegerField(default=0)

    def __str__(self):
        return '{}'.format(self.user)
    
    @receiver(post_save, sender=User)
    def create_gambler(sender, instance, created, **kwargs):
        if created:
            Gambler.objects.create(user=instance, balance=0)

    @receiver(post_save, sender=User)
    def save_gambler(sender, instance, **kwargs):
        instance.gambler.save()

class CoinBet(models.Model):
    heads_bet=IntegerField()
    tails_bet=IntegerField()
    name=IntegerField(primary_key=True)

    def __str__(self):
        return 'Bet Number: {}'.format(self.name)