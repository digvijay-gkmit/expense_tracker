# from django.core.mail import send_mail
from django.urls import reverse
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
import secrets
from django.core.cache import caches
from datetime import timedelta
from django.template.loader import render_to_string
from django.core.mail import EmailMessage

def send_verification_email(user, token, request):
    """
    Helper function to send verification email.
    """
    try:
        # Get the current site and construct the verification URL
        current_site = get_current_site(request)
        verification_url = reverse("verify-email", kwargs={"token": token})
        full_verification_url = f"http://{current_site.domain}{verification_url}"

        # Prepare email content
        email_subject = "Verify your email address"
        email_body = render_to_string(
            "email/verify_email.html",
            {
                "user": user,
                "verification_url": full_verification_url,
                "domain": current_site.domain,
            },
        )

        # Create and send email
        email = EmailMessage(
            subject=email_subject,
            body=email_body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[user.email],
        )
        email.content_subtype = "html"
        email.send(fail_silently=False)

    except Exception as e:
        print(f"Email sending failed: {str(e)}")
        # Optionally, handle the exception or raise it for further handling
        raise e


def generate_token_for_user(user):
    """
    Generate a secure token for user and store it in the cache.
    """
    token = secrets.token_urlsafe(32)
    token_cache = caches["token_cache"]
    token_cache.set(
        token, str(user.id), timeout=int(timedelta(minutes=1).total_seconds())
    )
    return token


def get_user_from_token(token):
    """
    Retrieve user ID from cache using token. Returns None if invalid.
    """
    token_cache = caches["token_cache"]
    user_id = token_cache.get(token)
    return user_id


def get_existing_token(user):
    """
    Helper method to check if an existing token is still valid for the given user.
    """
    token_cache = caches["token_cache"]
    for token in token_cache.keys():
        if token_cache.get(token) == str(user.id):
            return token
    return None