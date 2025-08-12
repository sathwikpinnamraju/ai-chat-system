from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .models import Chat
import google.generativeai as genai
from decouple import config

# Configure Gemini API
genai.configure(api_key=config("GEMINI_API_KEY"))

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def chat_with_ai(request):
    """
    Handles user chat messages, deducts tokens, and returns AI response from Gemini API.
    """

    message = request.data.get('message')
    if not message:
        return Response({"error": "Message is required."}, status=status.HTTP_400_BAD_REQUEST)

    user = request.user

    if user.tokens < 100:
        return Response({"error": "Insufficient tokens"}, status=status.HTTP_400_BAD_REQUEST)

    # Deduct tokens
    user.tokens -= 100
    user.save()

    try:
        # Call Gemini API
        model = genai.GenerativeModel("models/gemini-1.5-flash")
        response = model.generate_content(message)
        ai_response = response.text if hasattr(response, 'text') else str(response)

    except Exception as e:
        return Response({"error": f"AI service failed: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # Save chat history
    Chat.objects.create(user=user, message=message, response=ai_response)

    return Response({
        "message": message,
        "response": ai_response,
        "tokens_left": user.tokens
    }, status=status.HTTP_200_OK)
