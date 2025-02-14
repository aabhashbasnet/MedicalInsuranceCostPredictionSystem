
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
# model_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'Model', 'InsuranceCostPredictors.pkl')
# Load the pickled model
model = joblib.load(model_path)

@api_view(['POST'])
def predict(request):
    if request.method == 'POST':
        serializer = InsuranceSerializer(data=request.data) 
        if serializer.is_valid():
            input_data = tuple(serializer.validated_data.values())
            input_data_as_numpy_array = np.asarray(input_data)
            input_data_reshaped = input_data_as_numpy_array.reshape(1, -1)
            print(input_data_reshaped)
            prediction = model.predict(input_data_reshaped)
            insurance_data = serializer.save() 
            return Response({
                "prediction": prediction[0],
                "saved_data": {
                    "age": insurance_data.age,
                    "sex": insurance_data.get_sex_display(),  
                    "bmi": insurance_data.bmi,
                    "children": insurance_data.children,
                    "smoker": insurance_data.get_smoker_display(),  
                    "region": insurance_data.get_region_display()  
                }
            })
        else:
            return Response({"error": "Invalid input data", "details": serializer.errors}, status=400)




from django.http import JsonResponse
import math
from .responses import responses


# Default response when no match is found
default_response = "I'm sorry, I didn't understand that. Could you please rephrase or ask about insurance?"

# Predefined stop words
stop_words = set(["the", "is", "and", "or", "a", "an", "to", "in", "of", "for", "with", "on", "at", "by", "this", "that", "it"])

# Preprocess text: tokenize, lowercase, and remove stop words
def preprocess(text):
    tokens = text.lower().split()
    tokens = [word for word in tokens if word not in stop_words]
    return tokens

# Calculate Term Frequency (TF)
def compute_tf(tokens):
    tf = {}
    total_words = len(tokens)
    for word in tokens:
        tf[word] = tf.get(word, 0) + 1 / total_words
    return tf

# Calculate Inverse Document Frequency (IDF)
def compute_idf(documents):
    idf = {}
    total_documents = len(documents)
    for doc in documents:
        unique_words = set(doc)
        for word in unique_words:
            idf[word] = idf.get(word, 0) + 1
    for word, count in idf.items():
        idf[word] = math.log(total_documents / count)
    return idf

# Calculate TF-IDF
def compute_tfidf(tf, idf):
    tfidf = {}
    for word, tf_value in tf.items():
        tfidf[word] = tf_value * idf.get(word, 0)
    return tfidf

# Convert text to TF-IDF vector
def text_to_tfidf_vector(text, idf):
    tokens = preprocess(text)
    tf = compute_tf(tokens)
    tfidf = compute_tfidf(tf, idf)
    return tfidf

# Calculate cosine similarity between two TF-IDF vectors
def cosine_similarity(vec1, vec2):
    # Get all unique words from both vectors
    words = set(vec1.keys()).union(set(vec2.keys()))
    # Compute dot product
    dot_product = sum(vec1.get(word, 0) * vec2.get(word, 0) for word in words)
    # Compute magnitudes
    magnitude1 = math.sqrt(sum(vec1.get(word, 0) ** 2 for word in words))
    magnitude2 = math.sqrt(sum(vec2.get(word, 0) ** 2 for word in words))
    # Avoid division by zero
    if magnitude1 == 0 or magnitude2 == 0:
        return 0
    return dot_product / (magnitude1 * magnitude2)

# Precompute IDF for all questions
questions = list(responses.keys())
tokenized_questions = [preprocess(q) for q in questions]
idf = compute_idf(tokenized_questions)

def chatbot(request):
    user_input = request.GET.get('user_input', '').strip().lower()

    if user_input:
        # Convert user input to TF-IDF vector
        user_vector = text_to_tfidf_vector(user_input, idf)

        # Find the best matching question
        best_match = None
        best_score = -1

        for question in questions:
            question_vector = text_to_tfidf_vector(question, idf)
            score = cosine_similarity(user_vector, question_vector)
            if score > best_score:
                best_score = score
                best_match = question

        # If the best score is above a threshold, return the corresponding response
        if best_score > 0.2:  # You can adjust this threshold
            response = responses[best_match]
        else:
            response = default_response
    else:
        response = "Please ask me a question."

    return JsonResponse({'response': response})


from io import BytesIO
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet

@api_view(['POST'])
def download_report(request):
    """
    Generate and download a beautifully styled PDF report based on the prediction details.
    """
    try:
        # Retrieve data from request
        data = request.data
        age = data.get('age', 'N/A')
        sex = data.get('sex', 'N/A')
        bmi = data.get('bmi', 'N/A')
        children = data.get('children', 'N/A')
        smoker = data.get('smoker', 'N/A')
        region = data.get('region', 'N/A')
        prediction = float(data.get('predicted_cost', 0))  # Ensure prediction is a float

        # Create a buffer to hold the PDF data
        buffer = BytesIO()

        # Create a SimpleDocTemplate object with buffer and page size
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        elements = []

        # Set up styles
        styles = getSampleStyleSheet()
        title_style = styles['Title']
        title_style.fontName = 'Helvetica-Bold'
        title_style.fontSize = 18
        title_style.textColor = colors.darkblue

        normal_style = styles['Normal']
        normal_style.fontSize = 10

        # Add a stylish title to the report
        title = Paragraph("Medical Insurance Cost Prediction Report", title_style)
        elements.append(title)

        # Add space after the title
        elements.append(Paragraph("<br/><br/>", normal_style))

        # Add a subtitle or introduction
        subtitle = Paragraph("Here are the details of your medical insurance cost prediction.", normal_style)
        elements.append(subtitle)

        # Add space after the introduction
        elements.append(Paragraph("<br/><br/>", normal_style))

        # Prepare table data with enhanced formatting
        table_data = [
            ['Field', 'Value'],
            ['Age', str(age)],
            ['Sex', str(sex)],
            ['BMI', str(bmi)],
            ['Children', str(children)],
            ['Smoker', str(smoker)],
            ['Region', str(region)],
            ['Predicted Insurance Cost', f"${prediction:.2f}"]
        ]

        # Create a Table with the data and set the styles for each column
        table = Table(table_data, colWidths=[200, 200])
        
        # Table styling
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.navy),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
            ('ALIGN', (0, 1), (-1, -1), 'CENTER'),
            ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.grey),
        ]))

        # Add the table to the document
        elements.append(table)

        # Add a footer or notes
        footer = Paragraph("<br/><br/><i>Thank you for using our service. If you have any questions, feel free to contact us.</i>", normal_style)
        elements.append(footer)

        # Build the PDF
        doc.build(elements)

        # Retrieve PDF data from the buffer
        pdf_data = buffer.getvalue()
        buffer.close()

        # Create the HTTP response and return the PDF
        response = HttpResponse(pdf_data, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="insurance_prediction_report.pdf"'
        return response

    except Exception as e:
        print("Error generating report:", str(e))
        return HttpResponse("Failed to generate report. Please try again.", status=500)
