
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
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Predefined responses and corresponding answers
responses = {
    "Hi": "Hello! How can I assist you with insurance-related queries today?",
    "Does smoking affect my insurance costs?": "Yes, smoking significantly impacts your insurance cost. Smokers are at a higher risk of developing health issues, leading to increased medical expenses. Insurance providers consider this risk when calculating premiums, resulting in higher costs for smokers compared to non-smokers.",
    "How do I calculate my insurance cost?": "You can calculate your insurance cost using our prediction system. Please provide your details such as age, sex, BMI, number of children, smoking status, and region.",
    "What is BMI?": "BMI stands for Body Mass Index, a measure of body fat based on height and weight. It helps assess whether you're underweight, normal weight, overweight, or obese.",
    "What is a smoker discount?": "A smoker discount is usually a reduction in premium offered to non-smokers. Smoking significantly impacts health risks, which in turn affects insurance costs.",
    
    # Additional responses:
    "What factors influence insurance premiums?": "Several factors can influence insurance premiums, including your age, BMI, smoking habits, the number of dependents, and the region you live in. Insurance companies assess these factors to estimate the risk and determine the premium.",
    "Can I get insurance if I have pre-existing conditions?": "Yes, you can still get insurance with pre-existing conditions. However, it may result in higher premiums, as insurers may consider the risk associated with your condition.",
    "How often should I update my insurance information?": "It's recommended to update your insurance information whenever there is a significant change in your health, lifestyle, or family circumstances, such as changes in age, smoking habits, or the number of dependents.",
    "What is the difference between term insurance and whole life insurance?": "Term insurance provides coverage for a specific period, such as 10 or 20 years, and offers no cash value. Whole life insurance provides lifetime coverage and includes an investment component that builds cash value over time.",
    "What does deductible mean in insurance?": "A deductible is the amount you pay out-of-pocket for medical expenses before your insurance coverage kicks in. A higher deductible usually results in a lower premium, but you'll have to pay more upfront in case of a claim.",
    "Can I change my insurance plan?": "Yes, you can change your insurance plan, usually during an open enrollment period or after a qualifying life event (e.g., marriage, birth of a child, loss of other coverage).",
    "What is an insurance premium?": "An insurance premium is the amount you pay for your insurance coverage. It can be paid monthly, quarterly, or annually, and is based on factors like your risk profile, coverage amount, and policy type.",
    "What does 'out-of-pocket maximum' mean?": "An out-of-pocket maximum is the most you'll have to pay for covered services in a policy period (usually a year). After you reach this limit, your insurance will pay 100% of your covered expenses.",
    "Is health insurance mandatory?": "In many countries, health insurance is mandatory, especially for individuals who are self-employed or do not receive insurance through an employer. Laws vary by region, so it's important to check local regulations.",
    
    # Add more as needed...
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
        threshold = 0.3
        if best_match_score >= threshold:
            response = responses[list(responses.keys())[best_match_index]]
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
