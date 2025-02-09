
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

    print("Received data:", request.data)

    try:
        prediction = float(request.data.get('prediction', 0))  # Use `.get()` to avoid KeyError
    except ValueError:
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
from django.http import JsonResponse
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Predefined responses and corresponding answers
responses = {
    "Hi": "Hello! How can I assist you with insurance-related queries today?",
    "Does smoking affect my insurance costs?": "Yes, smoking significantly impacts your insurance cost. Smokers are at a higher risk of developing health issues, leading to increased medical expenses. Insurance providers consider this risk when calculating premiums, resulting in higher costs for smokers compared to non-smokers.",
    "How do I calculate my insurance cost?": "You can calculate your insurance cost using our prediction system. Please provide your details such as age, sex, BMI, number of children, smoking status, and region.",
    "What is BMI?": "BMI stands for Body Mass Index, a measure of body fat based on height and weight. It helps assess whether you're underweight, normal weight, overweight, or obese.",
    "What is a smoker discount?": "A smoker discount is usually a reduction in premium offered to non-smokers. Smoking significantly impacts health risks, which in turn affects insurance costs.",
    # Add more responses here
}

# Default fallback response
default_response = "I'm sorry, I didn't understand that. Could you please rephrase or ask about insurance?"

def chatbot(request):
    user_input = request.GET.get('user_input', '')  # Get user input from query params

    if user_input:
        # Combine user input with predefined responses
        texts = list(responses.keys()) + [user_input]
        
        # Convert text to vectors using TF-IDF
        tfidf_vectorizer = TfidfVectorizer().fit_transform(texts)
        cosine_sim = cosine_similarity(tfidf_vectorizer[-1], tfidf_vectorizer[:-1])

        # Find the most similar response based on cosine similarity
        best_match_index = cosine_sim.argmax()
        best_match_score = cosine_sim[0, best_match_index]  # Similarity score of the best match

        # Set a similarity threshold
        threshold = 0.5
        if best_match_score >= threshold:
            response = responses[list(responses.keys())[best_match_index]]
        else:
            response = default_response
    else:
        response = "Please ask me a question."

    return JsonResponse({'response': response})




