from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.hashers import make_password
from .models import User

@api_view(['POST'])
def register_user(request):
    """
    Registers a new user with 4000 starting tokens.
    """
    username = request.data.get('username')
    password = request.data.get('password')

    if not username or not password:
        return Response({"error": "Username and password are required."}, status=status.HTTP_400_BAD_REQUEST)

    if User.objects.filter(username=username).exists():
        return Response({"error": "Username already taken."}, status=status.HTTP_400_BAD_REQUEST)

    user = User.objects.create(
        username=username,
        password=make_password(password),
        tokens=4000
    )

    return Response({
        "message": "User registered successfully",
        "username": user.username,
        "tokens": user.tokens
    }, status=status.HTTP_201_CREATED)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def token_balance(request):
    """
    Returns the token balance of the authenticated user.
    """
    return Response({"tokens": request.user.tokens}, status=status.HTTP_200_OK)
