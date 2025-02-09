# chatbot/views.py
from django.http import JsonResponse
from .chatbot import chatbot_response

def chatbot_view(request):
    user_input = request.GET.get('user_input')  # Get user input from request
    response = chatbot_response(user_input)  # Call the chatbot function
    return JsonResponse({"response": response})  # Return the response as JSON
