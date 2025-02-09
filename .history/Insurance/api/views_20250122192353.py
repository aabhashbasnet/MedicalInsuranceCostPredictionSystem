
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
import numpy as np
import joblib
import os
from .serializers import InsuranceSerializer
from .models import Insurance  # Import your Insurance model

# Get the path to the pickled model file
model_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'Model', 'InsuranceCostPredictor.pkl')

# Load the pickled model
model = joblib.load(model_path)

@api_view(['POST'])
def predict(request):
    if request.method == 'POST':
        # Deserialize the input data from the request
        serializer = InsuranceSerializer(data=request.data)
        
        if serializer.is_valid():
            # Convert the input data to the input format for the model
            input_data = tuple(serializer.validated_data.values())
            input_data_as_numpy_array = np.asarray(input_data)
            input_data_reshaped = input_data_as_numpy_array.reshape(1, -1)
            
            # Print to check if the reshaping is correct
            print(input_data_reshaped)
            
            # Make a prediction using the model
            prediction = model.predict(input_data_reshaped)
            
            # Save the input data to the database
            insurance_data = serializer.save()  # Save the validated data to the database

            # Return the prediction and the saved data as a JSON response
            return Response({
                "prediction": prediction[0],
                "saved_data": {
                    "age": insurance_data.age,
                    "sex": insurance_data.get_sex_display(),  # Display the sex choice label (Male/Female)
                    "bmi": insurance_data.bmi,
                    "children": insurance_data.children,
                    "smoker": insurance_data.get_smoker_display(),  # Display the smoker choice label (Smoker/non-Smoker)
                    "region": insurance_data.get_region_display()  # Display the region choice label (Northeast/Southeast/etc.)
                }
            })
        else:
            # Return an error response if the serializer is invalid
            return Response({"error": "Invalid input data", "details": serializer.errors}, status=400)

from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from io import BytesIO
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from reportlab.lib.styles import getSampleStyleSheet

@csrf_exempt
@api_view(['POST'])
def download_report(request):
    # Get the data sent from the frontend (form input and prediction result)
    data = request.data  # Assuming you're using DRF

    # Ensure that 'prediction' is converted to float if it's a string
    try:
        prediction = float(data['prediction'])
    except ValueError:
        # In case of invalid input, default to 0.0
        prediction = 0.0

    # Create a BytesIO buffer to write the PDF
    buffer = BytesIO()

    # Set up PDF document with a title
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []

    # Add the title
    styles = getSampleStyleSheet()
    title = Paragraph("Medical Insurance Cost Prediction System", styles['Title'])
    elements.append(title)

    # Add a space after the title
    elements.append(Paragraph("<br/><br/>", styles['Normal']))

    # Create the data for the table (headers and values)
    data_for_table = [
        ['Field', 'Value'],
        ['Age', str(data['age'])],
        ['Sex', data['sex']],
        ['BMI', str(data['bmi'])],
        ['Children', str(data['children'])],
        ['Smoker', data['smoker']],
        ['Region', data['region']],
        ['Predicted Insurance Cost', f"${prediction:.2f}"]  # Format the prediction as a float
    ]

    # Create the table and apply styles
    table = Table(data_for_table)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))

    # Add the table to the document
    elements.append(table)

    # Build the PDF
    doc.build(elements)

    # Get the value of the BytesIO buffer
    pdf_data = buffer.getvalue()
    buffer.close()

    # Return the PDF as an HTTP response with the appropriate content type
    response = HttpResponse(pdf_data, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=insurance_report.pdf'
    return response

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Sample dataset of questions and answers
faq_data = {
    "How do I calculate my insurance cost?": "Insurance cost is calculated based on factors like age, sex, BMI, children, smoker status, and region.",
    "What factors affect my insurance cost?": "Age, sex, BMI, number of children, smoking habits, and region.",
    "How can I update my profile?": "You can update your profile details by logging into your account and editing your personal information.",
    "What is BMI and how does it affect my insurance cost?": "BMI stands for Body Mass Index, and a higher BMI may increase your insurance premium."
}

# Preprocess the queries and answers
questions = list(faq_data.keys())
answers = list(faq_data.values())

# Initialize TF-IDF Vectorizer
vectorizer = TfidfVectorizer()

# Convert the questions into a TF-IDF matrix
tfidf_matrix = vectorizer.fit_transform(questions)

# Function to get the most relevant answer based on cosine similarity
def chatbot_response(user_input):
    # Vectorize the user input
    user_input_vec = vectorizer.transform([user_input])
    
    # Calculate cosine similarity between user input and predefined questions
    cosine_sim = cosine_similarity(user_input_vec, tfidf_matrix)
    
    # Get the index of the most similar question
    most_similar_index = np.argmax(cosine_sim)
    
    # Return the corresponding answer
    return answers[most_similar_index]

# Example usage
user_input = "How is my insurance cost calculated?"
response = chatbot_response(user_input)
print(f"Chatbot: {response}")

