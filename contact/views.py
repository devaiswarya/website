# from django.shortcuts import render
# # Create your views here.
# from rest_framework.decorators import api_view
# from rest_framework.response import Response
# from rest_framework import status
# from django.core.mail import send_mail
# from django.conf import settings
# from datetime import datetime, timezone
# from .serializer import ContactSerializer
# from project.mongodb import contact_collection

# # contact_collection = db["contact_collection"]


# @api_view(["POST"])
# def create_contact(request):

#     serializer = ContactSerializer(data=request.data)

#     if not serializer.is_valid():

#         return Response(
#             {
#                 "message": "Invalid details",
#                 "errors": serializer.errors
#             },
#             status=status.HTTP_400_BAD_REQUEST
#         )

#     data = serializer.validated_data

#     # Step 1: Store details in MongoDB

#     contact_data = {
#         "name": data["name"],
#         "email": data["email"],
#         "phone": data["phone"],
#         "subject": data["subject"],
#         "message": data["message"],
#         "status": "New",
#         "created_at": datetime.now(timezone.utc)
#     }

#     result = contact_collection.insert_one(contact_data)

#     # Step 2: Prepare email content

#     email_subject = f"New Contact Enquiry - {data['subject']}"

#     email_message = f"""
#     New Contact Form Submission

#     Name: {data['name']}

#     Email: {data['email']}

#     Phone: {data['phone']}

#     Subject: {data['subject']}

#     Message: {data['message']}
#     """

#     # Step 3: Send email to admin

#     try:

#         send_mail(
#             subject=email_subject,
#             message=email_message,
#             from_email=settings.DEFAULT_FROM_EMAIL,
#             recipient_list=["joshibaaloinfotech@gmail.com"],
#             fail_silently=False
#         )

#         return Response(
#             {
#                 "message": "Contact details saved and email sent successfully",
#                 "contact_id": str(result.inserted_id)
#             },
#             status=status.HTTP_201_CREATED
#         )

#     except Exception as e:

#         return Response(
#             {
#                 "message": "Contact details saved, but email sending failed",
#                 "contact_id": str(result.inserted_id)
#             },
#             status=status.HTTP_201_CREATED
#         )


# from rest_framework.decorators import api_view
# from rest_framework.response import Response
# from rest_framework import status

# from django.core.mail import send_mail
# from django.conf import settings

# from datetime import datetime, timezone

# from .serializer import ContactSerializer



# @api_view(["POST"])
# def create_contact(request):

#     serializer = ContactSerializer(data=request.data)

#     if not serializer.is_valid():
#         return Response(
#             {
#                 "message": "Invalid details",
#                 "errors": serializer.errors
#             },
#             status=status.HTTP_400_BAD_REQUEST
#         )

#     data = serializer.validated_data

#     # Step 1: Save contact details in MongoDB

#     contact_data = {
#         "name": data["name"],
#         "email": data["email"],
#         "phone": data["phone"],
#         "subject": data["subject"],
#         "message": data["message"],
#         "status": "New",
#         "created_at": datetime.now(timezone.utc)
#     }

#     result = contact_collection.insert_one(contact_data)

#     # Step 2: Prepare email

#     email_subject = f"New Contact Enquiry - {data['subject']}"

#     email_message = f"""
#     New Contact Form Submission

#     Name: {data['name']}
#     Email: {data['email']}
#     Phone: {data['phone']}
#     Subject: {data['subject']}
#     Message: {data['message']}
#     """

#     # Step 3: Send email

#     try:

#         sent = send_mail(
#             subject=email_subject,
#             message=email_message,
#             from_email=settings.DEFAULT_FROM_EMAIL,
#             recipient_list=["joshibaaloinfotech@gmail.com"],
#             fail_silently=False
#         )

#         if sent == 1:
#             return Response(
#                 {
#                     "message": "Contact saved and email sent successfully",
#                     "contact_id": str(result.inserted_id)
#                 },
#                 status=status.HTTP_201_CREATED
#             )

#         raise Exception("Email was not accepted for sending")

#     except Exception as e:

#         print("EMAIL SENDING ERROR:", repr(e))

#         return Response(
#             {
#                 "message": "Contact details saved, but email sending failed",
#                 "contact_id": str(result.inserted_id),
#                 "email_error": str(e)
#             },
#             status=status.HTTP_201_CREATED
#         )



# from rest_framework.decorators import api_view
# from rest_framework.response import Response
# from rest_framework import status
# from datetime import datetime, timezone
# from django.conf import settings
# from project.mongodb import contact_collection
# from utils.email_service import send_contact_email
# from .serializer import ContactSerializer


# @api_view(["POST"])
# def create_contact(request):

#     serializer = ContactSerializer(data=request.data)

#     if not serializer.is_valid():
#         return Response(
#             {
#                 "message": "Invalid details",
#                 "errors": serializer.errors
#             },
#             status=status.HTTP_400_BAD_REQUEST
#         )

#     data = serializer.validated_data

#     # Step 1: Save contact details in MongoDB

#     contact_data = {
#         "name": data["name"],
#         "email": data["email"],
#         "phone": data["phone"],
#         "subject": data["subject"],
#         "message": data["message"],
#         "status": "New",
#         "created_at": datetime.now(timezone.utc)
#     }

#     result = contact_collection.insert_one(contact_data)

#     # Step 2: Prepare email

#     email_subject = f"New Contact Enquiry - {data['subject']}"

#     email_message = f"""
# New Contact Form Submission

# Name: {data['name']}
# Email: {data['email']}
# Phone: {data['phone']}
# Subject: {data['subject']}
# Message: {data['message']}
# """

#     # Step 3: Send email using Resend API

#     email_result = send_contact_email(
#         subject=email_subject,
#         message=email_message
#     )

#     # Step 4: Return response

#     if email_result["success"]:

#         return Response(
#             {
#                 "message": "Contact saved and email sent successfully",
#                 "contact_id": str(result.inserted_id),
#                 "email_id": email_result["email_id"]
#             },
#             status=status.HTTP_201_CREATED
#         )

#     return Response(
#         {
#             "message": "Contact details saved, but email sending failed",
#             "contact_id": str(result.inserted_id),
#             "email_error": email_result["error"]
#         },
#         status=status.HTTP_201_CREATED
#     )


from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .serializer import ContactSerializer
from utils.email_service import send_contact_email


@api_view(["POST"])
def create_contact(request):

    serializer = ContactSerializer(data=request.data)

    if not serializer.is_valid():

        return Response(
            {
                "message": "Validation failed",
                "errors": serializer.errors
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    data = serializer.validated_data

    try:

        email_response = send_contact_email(
            name=data["name"],
            email=data["email"],
            phone=data["phone"],
            subject=data["subject"],
            message=data["message"]
        )

        return Response(
            {
                "message": "Contact enquiry submitted and email sent successfully",
                "email_response": str(email_response)
            },
            status=status.HTTP_201_CREATED
        )

    except Exception as e:

        print("Email sending failed:", str(e))

        return Response(
            {
                "message": "Contact enquiry received, but email sending failed"
            },
            status=status.HTTP_201_CREATED
        )