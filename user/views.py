from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status

from rest_framework_simplejwt.tokens import RefreshToken

from django.contrib.auth.hashers import check_password, make_password

from .serializer import LoginSerializer, RegisterSerializer
from project.mongodb import users_collection

from datetime import datetime, timezone, timedelta


@api_view(['POST'])
@permission_classes([AllowAny])
def register_api(request):

    # Step 1: Validate incoming data
    serializer = RegisterSerializer(data=request.data)

    if not serializer.is_valid():
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    # Step 2: Get user details
    name = serializer.validated_data['name']
    email = serializer.validated_data['email'].lower()
    password = serializer.validated_data['password']

    # Step 3: Check email already exists
    existing_user = users_collection.find_one({
        "email": email
    })

    if existing_user:
        return Response({
            "message": "Email already registered"
        }, status=status.HTTP_409_CONFLICT)

    # Step 4: Hash the password
    hashed_password = make_password(password)

    # Step 5: Create user document
    user_data = {
        "name": name,
        "email": email,
        "password": hashed_password,
        "created_at": datetime.now(timezone.utc)
    }

    # Step 6: Insert into MongoDB
    result = users_collection.insert_one(user_data)

    # Step 7: Return response
    return Response({
        "message": "Registration successful",
        "user": {
            "id": str(result.inserted_id),
            "name": name,
            "email": email
        }
    }, status=status.HTTP_201_CREATED)

@api_view(['POST'])
# @permission_classes([AllowAny])
def login_api(request):

    # Step 1: Validate incoming data
    serializer = LoginSerializer(data=request.data)

    if not serializer.is_valid():
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    # Step 2: Get email and password
    email = serializer.validated_data['email'].lower()
    password = serializer.validated_data['password']
    remember_me = serializer.validated_data['remember_me']

    # Step 3: Find user in MongoDB
    user = users_collection.find_one({
        "email": email
    })

    if not user:
        return Response({
            "message": "Invalid email or password"
        }, status=status.HTTP_401_UNAUTHORIZED)

    # Step 4: Check password
    if not check_password(password, user['password']):
        return Response({
            "message": "Invalid email or password"
        }, status=status.HTTP_401_UNAUTHORIZED)

    # Step 5: Generate JWT tokens
    refresh = RefreshToken()

    refresh['user_id'] = str(user['_id'])
    refresh['email'] = user['email']

    # Step 6: Remember Me token expiry
    if remember_me:
        refresh.set_exp(
            lifetime=timedelta(days=30)
        )

    access_token = refresh.access_token

    # Step 7: Return response
    return Response({
        "message": "Login successful",
        "user": {
            "id": str(user['_id']),
            "email": user['email']
        },
        "tokens": {
            "refresh": str(refresh),
            "access": str(access_token)
        }
    }, status=status.HTTP_200_OK)
