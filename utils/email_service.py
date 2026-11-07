import resend
from django.conf import settings


def send_contact_email(subject, message):

    resend.api_key = settings.RESEND_API_KEY

    params = {
        "from": settings.DEFAULT_FROM_EMAIL,
        "to": [settings.CONTACT_RECEIVER_EMAIL],
        "subject": subject,
        "html": f"<p>{message}</p>"
    }

    response = resend.Emails.send(params)

    return {
        "success": True,
        "email_id": response["id"]
    }