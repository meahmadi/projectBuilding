# users/signals.py
from django.conf import settings
from django.contrib.auth.models import User
from allauth.account.signals import user_logged_in
from django.dispatch import receiver

# Specify the GitHub username or email for the admin user
GITHUB_ADMIN_USERNAME = "meahmadi"  # Replace with the desired GitHub username
GITHUB_ADMIN_EMAIL = "me.ahmadi@gmail.com"        # Optionally, use an email instead

@receiver(user_logged_in)
def make_admin_on_github_login(sender, request, user, **kwargs):
    # Check if the logged-in user matches the GitHub admin username or email
    if user.username == GITHUB_ADMIN_USERNAME or user.email == GITHUB_ADMIN_EMAIL:
        user.is_staff = True  # Allows access to Django admin
        user.is_superuser = True  # Grants superuser privileges
        user.save()
