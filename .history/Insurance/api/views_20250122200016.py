
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
from django.http import JsonResponse
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Predefined responses and corresponding answers
responses = {
    "Does smoking affect my insurance cost"
    "How do I calculate my insurance cost?": "You can calculate your insurance cost using our prediction system. Please provide your details such as age, sex, BMI, number of children, smoking status, and region.",
    "What is BMI?": "BMI stands for Body Mass Index, a measure of body fat based on height and weight. It helps assess whether you're underweight, normal weight, overweight, or obese.",
    "What is a smoker discount?": "A smoker discount is usually a reduction in premium offered to non-smokers. Smoking significantly impacts health risks, which in turn affects insurance costs.",
    "What factors affect insurance cost?": "Insurance costs are influenced by age, sex, BMI, number of children, smoking status, and region. Lifestyle choices and health conditions also play a role.",
    "What is health insurance?": "Health insurance is a type of insurance that covers medical expenses. It helps protect you financially in case of illness or injury.",
    "Why is insurance important?": "Insurance provides financial protection against unforeseen events such as medical emergencies. It ensures peace of mind and access to healthcare when needed.",
    "What is a premium?": "A premium is the amount you pay to your insurance provider, usually monthly or annually, to keep your policy active.",
    "What is deductible in insurance?": "A deductible is the amount you pay out of pocket before your insurance starts covering expenses. Higher deductibles usually mean lower premiums.",
    "Can I predict my insurance cost without signing up?": "You can use our insurance cost prediction system without signing up. However, signing up lets you save your data and access personalized recommendations.",
    "What is a region in insurance terms?": "Region refers to the geographical area where you live. It impacts insurance costs due to variations in healthcare costs and risk factors.",
    "How accurate is the insurance prediction?": "Our insurance prediction is based on machine learning models trained on reliable datasets. While it is highly accurate, the results may vary slightly from actual costs.",
    "Is my data secure?": "Yes, your data is secure with us. We follow strict data protection policies to ensure your privacy and security.",
    "Can I update my details later?": "Yes, you can update your personal details anytime by logging into your account.",
    "What happens if I smoke occasionally?": "Occasional smoking may still impact your insurance cost. Be honest while filling in your details to get accurate predictions.",
    "What is the minimum age for insurance?": "The minimum age for health insurance depends on the provider, but most policies cover individuals from birth with a parent or guardian's consent.",
    "Can I get family insurance?": "Yes, you can opt for family health insurance, which covers multiple members under a single policy.",
    "What documents are required for insurance?": "Documents like ID proof, address proof, and medical history may be required while applying for insurance.",
    "What if I don't have health issues?": "Even if you're healthy, insurance provides a safety net for unexpected medical emergencies and helps cover rising healthcare costs.",
    "Does insurance cover all diseases?": "Insurance policies typically cover most diseases, but pre-existing conditions or specific illnesses may have a waiting period or exclusions.",
    "Can I cancel my insurance policy?": "Yes, you can cancel your policy. Some providers offer a free look period for cancellation without penalties."
}


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
        response = responses[list(responses.keys())[best_match_index]]
    else:
        response = "Please ask me a question."

    return JsonResponse({'response': response})



