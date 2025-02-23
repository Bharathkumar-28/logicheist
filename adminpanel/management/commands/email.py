# send_inactive_emails.py

import datetime
from django.core.mail import send_mail
from django.core.management.base import BaseCommand
from django.conf import settings
from django.utils import timezone  # Import Django's timezone utility
from django.contrib.auth.models import User  # Import User model to get email
from adminpanel.models import UserActivity  # Import UserActivity model

class Command(BaseCommand):
    help = "Send an email to inactive users who haven't been active for more than 30 seconds"

    def handle(self, *args, **kwargs):
        # Get the current time as timezone-aware datetime
        current_time = timezone.now()
        thirty_seconds_ago = current_time - datetime.timedelta(seconds=30)  # Adjust for quick testing

        # Get users who haven't been active for more than 30 seconds
        # This joins UserActivity with User and filters users based on the last_active time
        inactive_users = UserActivity.objects.filter(last_active__lt=thirty_seconds_ago)

        # Check if any inactive users are found
        if not inactive_users:
            self.stdout.write(self.style.SUCCESS("No inactive users found."))
            return

        # Define email content
        subject = "We Miss You!"
        message = "Hello, we noticed you haven't been active for a while. Come back and check out what's new!"
        from_email = settings.EMAIL_HOST_USER

        # Loop through inactive users and send email
        for user_activity in inactive_users:
            user_email = user_activity.user.email  # Access the User's email via the related User object
            send_mail(subject, message, from_email, [user_email])

            # Log the email sending status
            self.stdout.write(self.style.SUCCESS(f"Email successfully sent to {user_email}"))
