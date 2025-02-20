from django.core.management.base import BaseCommand  # Base class for Django commands
from django.core.mail import send_mail  # Function to send emails
from django.contrib.auth.models import User  # User model (to get all users)
from django.conf import settings  # To access settings like DEFAULT_FROM_EMAIL

class Command(BaseCommand):
    help = 'Send an email to all users'

    def handle(self, *args, **kwargs):
        users = User.objects.all()  # Get all users from the database
        subject = 'Your Email Subject'  # Email subject
        message = 'This is the body of the email.'  # Email content
        from_email = settings.DEFAULT_FROM_EMAIL  # Use the default email address from settings

        # Loop through each user and send them the email
        for user in users:
            send_mail(
                subject,  # Email subject
                message,  # Email body
                from_email,  # From email address
                [user.email],  # To email address (user's email)
            )

        self.stdout.write(self.style.SUCCESS('Successfully sent emails to all users.'))  # Success message
