# import resend
# from django.conf import settings


# def send_contact_email(subject, message):

#     resend.api_key = settings.RESEND_API_KEY

#     params = {
#         "from": settings.DEFAULT_FROM_EMAIL,
#         "to": [settings.CONTACT_RECEIVER_EMAIL],
#         "subject": subject,
#         "html": f"<p>{message}</p>"
#     }

#     response = resend.Emails.send(params)

#     return {
#         "success": True,
#         "email_id": response["id"]
#     }

# import resend
# from django.conf import settings

# def send_contact_email(email, name, message):

#     resend.api_key = settings.RESEND_API_KEY

#     params = {
#         "from": "ALO Website <onboarding@resend.dev>",
#         "to": ["your-email@gmail.com"],
#         "subject": "New Contact Form Submission",
#         "html": f"""
#             <h2>New Contact</h2>
#             <p>Name: {name}</p>
#             <p>Email: {email}</p>
#             <p>Message: {message}</p>
#         """
#     }

#     return resend.Emails.send(params)


# import resend
# from django.conf import settings


# def send_contact_email(name, email, phone, subject, message):

#     resend.api_key = settings.RESEND_API_KEY

#     params = {
#         "from": "ALO Website <onboarding@resend.dev>",
#         "to": ["joshibaaloschool@gmail.com"],
#         "subject": subject,

#         "html": f"""
#             <h2>New Contact Form Enquiry</h2>

#             <p><b>Name:</b> {name}</p>
#             <p><b>Email:</b> {email}</p>
#             <p><b>Phone:</b> {phone}</p>
#             <p><b>Subject:</b> {subject}</p>
#             <p><b>Message:</b> {message}</p>
#         """
#     }

#     response = resend.Emails.send(params)

#     return response


import resend
from django.conf import settings


def send_contact_email(name, email, phone, subject, message):

    if not settings.RESEND_API_KEY:
        raise ValueError("RESEND_API_KEY is missing")

    resend.api_key = settings.RESEND_API_KEY

    params = {
        "from": f"ALO Website <{settings.DEFAULT_FROM_EMAIL}>",

        # "to": [settings.CONTACT_RECEIVER_EMAIL],

        "to": ["aiswaryabalu88@gmail.com"],

        "subject": f"New Contact Enquiry: {subject}",

        "html": f"""
            <h2>New Contact Form Enquiry</h2>

            <p><b>Name:</b> {name}</p>
            <p><b>Email:</b> {email}</p>
            <p><b>Phone:</b> {phone}</p>
            <p><b>Subject:</b> {subject}</p>
            <p><b>Message:</b> {message}</p>
        """
    }

    response = resend.Emails.send(params)

    return response