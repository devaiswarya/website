from django.shortcuts import render
# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import send_mail
from django.conf import settings
from datetime import datetime, timezone
from .serializer import ContactSerializer
from project.mongodb import contact_collection

# contact_collection = db["contact_collection"]


@api_view(["POST"])
def create_contact(request):

    serializer = ContactSerializer(data=request.data)

    if not serializer.is_valid():

        return Response(
            {
                "message": "Invalid details",
                "errors": serializer.errors
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    data = serializer.validated_data

    # Step 1: Store details in MongoDB

    contact_data = {
        "name": data["name"],
        "email": data["email"],
        "phone": data["phone"],
        "subject": data["subject"],
        "message": data["message"],
        "status": "New",
        "created_at": datetime.now(timezone.utc)
    }

    result = contact_collection.insert_one(contact_data)

    # Step 2: Prepare email content

    email_subject = f"New Contact Enquiry - {data['subject']}"

    email_message = f"""
    New Contact Form Submission

    Name: {data['name']}

    Email: {data['email']}

    Phone: {data['phone']}

    Subject: {data['subject']}

    Message: {data['message']}
    """

    # Step 3: Send email to admin

    try:

        send_mail(
            subject=email_subject,
            message=email_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=["joshibaaloinfotech@gmail.com"],
            fail_silently=False
        )

        return Response(
            {
                "message": "Contact details saved and email sent successfully",
                "contact_id": str(result.inserted_id)
            },
            status=status.HTTP_201_CREATED
        )

    except Exception as e:

        return Response(
            {
                "message": "Contact details saved, but email sending failed",
                "contact_id": str(result.inserted_id)
            },
            status=status.HTTP_201_CREATED
        )

