from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse

# Create your tests here.
class UserTest(TestCase):
    def setUp(self):        #This runs before every single test
        # Create user for each test
        User.objects.create(username='Testuser', password='password')       #creation of TEST user object
        self.user = User.objects.get(username='Testuser')
        self.user.set_password('new password')
        self.user.save()                                                    #saving the user object with new hashed password
    
    def tearDown(self):     #This runs after every single test
        # Clean up after each test
        self.user.delete()          #Deletion of the TEST user object
    
    def test_user_coma_gambler_has_gambler_attributes(self):
        self.assertEqual(self.user.gambler.balance, 0)          #Checks if Gambler object has right attribute balance with default amount set to 0
        self.assertIsInstance(self.user.gambler.id, int)        #Checks if Gambler object has unique primary key (int field)

    def test_coinflip_site(self):
        self.client.force_login(self.user)                  #Logging a Testuser into a webapp
        response = self.client.get(reverse('coinflip'))     #reading the /coinflip url
        self.assertEqual(response.status_code, 200)         #if the coinflip url exists
        self.assertEqual(response.context['heads_bet'], 0)  
        self.assertEqual(response.context['tails_bet'], 0)                  #Checking the every stuff_for_frontend dictionary position
        self.assertEqual(response.context['bet_value'], 'No flip yet')
        self.assertEqual(response.context['balance'], self.user.gambler.balance)

    def test_all_urls_without_logging(self):                #This test runs every url without logging in and checks if the url exists and has the
        response = self.client.get(reverse('coinflip'))     #right response like 'You are not logged in' if youre trying to access coinflip app
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'You are not logged in')
        response = self.client.get(reverse('free_balance'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'You are not logged in')
        response = self.client.get(reverse('new_message'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'You are not logged in')
        response = self.client.get(reverse('read_messages'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'You are not logged in')
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Log In')
        response = self.client.get(reverse('signup'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Sign Up')
    
    def test_free_balance_view(self):           #Test for free_balance url
        self.client.force_login(self.user)      #Logging the Testuser in
        self.client.get(reverse('free_balance'))    #Going into free_balance url
        response = self.client.get('')              
        self.assertContains(response, 'Your balance: 100')      #Checking if balance was increased by the right amount
    
    def test_message_views(self):           #Test for cipher message views
        self.client.force_login(self.user)  #Logging a Testuser
        response = self.client.get(reverse('new_message'))  #Checking if new_message url shows the right html file when youre logged in
        self.assertContains(response, 'Hi Testuser')        # -""-
        self.client.post(reverse('new_message'), data={'message': 'pozdrawiam'})    #Sending a form with message input of 'pozdrawiam'
        response = self.client.get(reverse('read_messages'))    #Getting the response of read_messages url while logged
        self.assertContains(response, 'pozdrawiam')             #Checking if created before messages is stored in database and is showing right html file

    def test_coinflip_view_normal_heads_bet(self):
        self.client.force_login(self.user)
        self.user.gambler.balance = 200     #balance = 200
        self.user.gambler.save()            #save the Testuser object
        response = self.client.post(reverse('coinflip'), data={'heads_bet': '100', 'tails_bet': ''})    #heads bet = 100 is less than balance = 200
        if response.context['bet_value'] == 'heads':                #if the flip was heads
            self.assertEqual(response.context['balance'], 300)      #checks if balance is displayed with the right amount = 300
        elif response.context['bet_value'] == 'tails':              #if the flip was tails
            self.assertEqual(response.context['balance'], 100)      #checks if balance is displayed with the right amount = 100
        
    def test_coinflip_view_normal_tails_bet(self):
        self.client.force_login(self.user)
        self.user.gambler.balance = 200     #balance = 200
        self.user.gambler.save()            #save the Testuser object
        response = self.client.post(reverse('coinflip'), data={'heads_bet': '', 'tails_bet': '100'})    #tails bet = 100 is less than balance = 200
        if response.context['bet_value'] == 'heads':                #if the flip was heads
            self.assertEqual(response.context['balance'], 100)      #checks if balance is displayed with the right amount = 100
        elif response.context['bet_value'] == 'tails':              #if the flip was tails
            self.assertEqual(response.context['balance'], 300)      #checks if balance is displayed with the right amount = 300
    
    def test_coinflip_view_negative_bets(self):
        self.client.force_login(self.user) #balance = 0
        response = self.client.post(reverse('coinflip'), data={'heads_bet': '-100', 'tails_bet': ''})          #negative heads bet
        self.assertEqual(response.context['bet_value'], 'No flip yet')                                         #website doesnt allow for this bet
        response = self.client.post(reverse('coinflip'), data={'heads_bet': '', 'tails_bet': '-100'})          #similar situation
        self.assertEqual(response.context['bet_value'], 'No flip yet')                                         #same response

    def test_coinflip_view_too_high_bets(self):
        self.client.force_login(self.user)
        self.user.gambler.balance = 200     #balance = 200
        self.user.gambler.save()            #save user object
        response = self.client.post(reverse('coinflip'), data={'heads_bet': '300', 'tails_bet': ''})        #bet is higher than balance
        self.assertEqual(response.context['bet_value'], 'No flip yet')                                      #website doesnt allow this bet
        self.assertEqual(response.context['balance'], 200)                                                  #balance is not changed
        response = self.client.post(reverse('coinflip'), data={'heads_bet': '', 'tails_bet': '300'})        #same action for tails bet
        self.assertEqual(response.context['bet_value'], 'No flip yet')
        self.assertEqual(response.context['balance'], 200)