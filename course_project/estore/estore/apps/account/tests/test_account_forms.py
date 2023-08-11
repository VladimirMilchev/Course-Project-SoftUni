from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from ..forms import UserAddressForm, RegistrationForm, PwdResetForm, PwdResetConfirmForm, UserEditForm
from ..models import Customer


class FormTests(TestCase):

    def test_user_address_form(self):
        form_data = {
            "full_name": "John Doe",
            "phone": "1234567890",
            "address_line": "123 Main St",
            "address_line2": "Apt 4B",
            "town_city": "City",
            "postcode": "12345",
        }
        form = UserAddressForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_registration_form(self):
        form_data = {
            "name": "newuser",
            "email": "newuser@example.com",
            "password": "password123",
            "password2": "password123",
        }
        form = RegistrationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_user_login_form_response(self):
        url = reverse('account:login')

        form_data = {
            "username": "a@a.com",
            "password": "GsH687#EYzcq",
        }

        response = self.client.post(url, form_data)
        self.assertEqual(response.status_code, 200)

    def test_pwd_reset_form(self):
        self.user = Customer.objects.create_user(name='testuser', email='user@example.com', password='password123')

        form_data = {
            "email": "user@example.com",
        }
        form = PwdResetForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_pwd_reset_confirm_form(self):
        form_data = {
            "new_password1": "newpassword123",
            "new_password2": "newpassword123",
        }
        form = PwdResetConfirmForm(data=form_data, user=User)
        self.assertTrue(form.is_valid())

    def test_user_edit_form(self):
        form_data = {
            "name": "updateduser",
            "email": "updated@example.com",
            "mobile": "08888888888",
        }
        form = UserEditForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_user_edit_form_not_valid(self):
        form_data = {
            "name": "updateduser",
            "email": "updated@example.com",
            "mobile": "0123456",
        }
        form = UserEditForm(data=form_data)
        self.assertFalse(form.errors)
