from django.urls import path
from . import views
urlpatterns = [
    path('predict/',views.predict,name='predict'),
V    path('chatbot/', views.chatbot, name='chatbot'),  # Add this line for the download report view

]