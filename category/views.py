from django.shortcuts import render
from rest_framework.decorators import api_view,parser_classes
from rest_framework.response import Response
from rest_framework import status
from .serializer import CategorySerializer
from project.mongodb import db
from datetime import datetime
from rest_framework.parsers import (MultiPartParser,FormParser)
from django.core.files.storage import default_storage
from project.mongodb import categories_collection


@api_view(["POST"])
def create_category(request):
    serializer = CategorySerializer(
        data=request.data
    )
    if not serializer.is_valid():
        return Response(
            {
                "message": serializer.errors
            },
            status=status.HTTP_400_BAD_REQUEST
        )
    name = serializer.validated_data["name"]
    parent_id = serializer.validated_data.get(
        "parent_id"
    )
    image = serializer.validated_data.get(
        "image"
    )
    description = serializer.validated_data.get(
        "description"
    )
    category_status = serializer.validated_data.get(
        "status",
        "Active"
    )
    category = {
        "name": name,
        "parent_id": parent_id,
        "image": image,
        "description": description,
        "status": category_status,
        "created_at": datetime.now()
    }
    result = categories_collection.insert_one(
        category
    )
    category_id = str(
        result.inserted_id
    )       
    return Response(
        {
            "message": "Category created successfully",
            "category_id": category_id,
            "name": name,
            "parent_id": parent_id,
            "image": image,
            "description": description,
            "status": category_status
        },
        status=status.HTTP_201_CREATED
    )


@api_view(["POST"])
@parser_classes([MultiPartParser, FormParser])
def upload_file(request):
    file = request.FILES.get("file")
    if not file:
        return Response(
            {"message": "File is required"},
            status=status.HTTP_400_BAD_REQUEST
        )
    file_path = default_storage.save(
        f"uploads/{file.name}",
        file
    )
    return Response(
        {
            "message": "File uploaded successfully",
            "file_name": file.name,
            "file_path": file_path,
            "file_url":f'http://127.0.0.1:8000/media/{file_path}'
        },
        status=status.HTTP_201_CREATED
    )


# @api_view(["POST"])
# @parser_classes([MultiPartParser, FormParser])
# def upload_file(request):

#     file = request.FILES.get("file")

#     if not file:
#         return Response(
#             {"message": "File is required"},
#             status=status.HTTP_400_BAD_REQUEST
#         )

#     try:
#         file_path = default_storage.save(
#             f"uploads/{file.name}",
#             file
#         )

#         file_url = request.build_absolute_uri(
#             default_storage.url(file_path)
#         )

#         return Response(
#             {
#                 "message": "File uploaded successfully",
#                 "file_name": file.name,
#                 "file_path": file_path,
#                 "file_url": file_url
#             },
#             status=status.HTTP_201_CREATED
#         )

#     except Exception as e:

#         return Response(
#             {
#                 "message": "File upload failed",
#                 "error": str(e)
#             },
#             status=status.HTTP_500_INTERNAL_SERVER_ERROR
#         )