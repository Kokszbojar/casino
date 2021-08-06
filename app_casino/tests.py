from django.forms.fields import CharField, IntegerField
from django.test import TestCase
from django.contrib.auth.models import User
from . import models

# Create your tests here.
class UserTest(TestCase):
    def setUp(self):
        # Create some users
        self.user_1 = User.objects.create(username='Testuser', password='pow123password')
    
    def test_user_coma_gambler_has_gambler_attributes(self):
        self.assertEqual(self.user_1.gambler.balance, 0)
        self.assertIsInstance(self.user_1.gambler.id, int)

    #def test_coinflip_bet_with_0_balance(self):


    def tearDown(self):
        # Clean up after each test
        self.user_1.delete()