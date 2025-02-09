from django.urls import path
from . import views
urlpatterns = [
    path('predict/',views.predict,name='predict'),
    path('adownload-report/', views.download_report, name='download_report'),
    path('chatbot/', views.chatbot, name='chatbot'),  # Add this line for the download report view

]