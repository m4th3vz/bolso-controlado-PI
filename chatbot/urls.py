# chatbot/urls.py
from django.urls import path
from .views import ChatbotView, ChatbotAPI

urlpatterns = [
    path('chatbot/', ChatbotView.as_view(), name='chatbot'),
    path('api/chat/', ChatbotAPI.as_view(), name='chatbot_api'),
]