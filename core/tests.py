from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from core.forms import RegisterForm
from core.models import AllowedEmail


class RegisterFormTests(TestCase):
    def test_rejects_uninvited_email(self):
        form = RegisterForm(data={
            "email": "random@example.com",
            "username": "random",
            "password": "strong-password-123",
            "password_confirm": "strong-password-123",
        })

        self.assertFalse(form.is_valid())
        self.assertIn("This email is not on the invite list.", form.non_field_errors())

    def test_accepts_invited_email(self):
        AllowedEmail.objects.create(email="invited@example.com")

        form = RegisterForm(data={
            "email": "invited@example.com",
            "username": "invited",
            "password": "strong-password-123",
            "password_confirm": "strong-password-123",
        })

        self.assertTrue(form.is_valid())


class RegistrationViewTests(TestCase):
    def test_successful_registration_marks_invite_used(self):
        invite = AllowedEmail.objects.create(email="new@example.com")

        response = self.client.post(reverse("register"), data={
            "email": "new@example.com",
            "username": "newuser",
            "password": "strong-password-123",
            "password_confirm": "strong-password-123",
        })

        self.assertRedirects(response, reverse("home"))
        self.assertTrue(User.objects.filter(username="newuser").exists())
        invite.refresh_from_db()
        self.assertTrue(invite.registered)
