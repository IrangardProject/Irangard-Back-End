from django.test import TestCase
from ..models import *

class UserTestCase(TestCase):

    def setUp(self):
        
        User.objects.create(
            email = "ghazal@gmail.com",
            username = "Ghazal",
            first_name = "غزل",
            last_name = "بخشنده",
            phone_no = "09225678765",
            password = '123456',
        )
        self.user_one = User.objects.create(
                email = "tahamsious@gmail.com",
                username = "tahmasioius",
                first_name = "غزل",
                last_name = "بخشنده",
                phone_no = "09225678765",
                password = '123456',
            )

        self.user_two = User.objects.create(
            email="ahamdreza@gmail.com",
            username="ahamdreza",
            first_name="غزل",
            last_name="بخشنده",
            phone_no="09225678765",
            password='123456',
        )

        self.special_user_one = SpecialUser.objects.create(user=self.user_one)

    def test_user_email(self):
        user = User.objects.get(username='Ghazal')
        self.assertEqual(user.email, 'ghazal@gmail.com')

    def test_user_phone_no(self):
        user = User.objects.get(email='ghazal@gmail.com')
        self.assertEqual(user.phone_no, '09225678765')
    
    def test_user_password(self):
        user = User.objects.get(username='Ghazal')
        self.assertEqual(user.password, '123456')

    def test_update_following_number(self):
        self.user_two.following.add(self.user_one)
        self.user_two.save()
        self.user_two.update_following_no()
        self.assertEqual(self.user_two.following_number, 1)

    def test_update_follower_number(self):
        self.user_two.following.add(self.user_one)
        self.user_two.save()
        self.user_one.update_follower_no()
        self.assertEqual(self.user_one.follower_number, 1)

    def test_increase_wallet_credit(self):
        self.user_one.increase_wallet_credit(10)
        self.assertEqual(self.user_one.wallet_credit, 10)

    def test_decrease_wallet_credit(self):
        self.user_one.wallet_credit = 100
        self.user_one.save()
        self.user_one.decrease_wallet_credit(10)
        self.assertEqual(self.user_one.wallet_credit, 90)

    def test_increase_diamond(self):
        self.user_one.increase_dimonds(10)
        self.assertEqual(self.user_one.dimonds, 10)

    def test_decrease_diamond(self):
        self.user_one.dimonds = 100
        self.user_one.save()
        self.user_one.decrease_dimonds(10)
        self.assertEqual(self.user_one.dimonds, 90)

    def test_special_user_get_follows(self):
        self.assertEqual(self.special_user_one.follows(self.user_two), False)

    def test_withdraw_money(self):
        self.special_user_one.total_revenue = 100
        self.special_user_one.save()
        self.special_user_one.withdraw(10)
        self.assertEqual(self.special_user_one.total_revenue, 90)

    def test_deposit_money(self):
        self.special_user_one.total_revenue = 100
        self.special_user_one.save()
        self.special_user_one.deposit(10)
        self.assertEqual(self.special_user_one.total_revenue, 110)

