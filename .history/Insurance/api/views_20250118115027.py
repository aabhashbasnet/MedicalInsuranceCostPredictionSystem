
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
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle
from io import BytesIO
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response

@csrf_exempt
@api_view(['POST'])
def download_report(request):
    # Get the data sent from the frontend
    data = request.data  # Assuming you're using DRF

    # Prepare the prediction value (ensure it is float for formatting)
    try:
        prediction = float(data['prediction'])  # Ensure prediction is a float
    except ValueError:
        prediction = 0.0

    # Create a BytesIO buffer to write the PDF
    buffer = BytesIO()

    # Create a SimpleDocTemplate for the PDF
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []

    # Style for the document
    from reportlab.lib.styles import getSampleStyleSheet
    styles = getSampleStyleSheet()

    # Add an introduction to the report
    intro_text = "This report summarizes the medical insurance cost prediction based on the user's input data. Please review the details below."
    intro_paragraph = Paragraph(intro_text, styles['Normal'])
    elements.append(intro_paragraph)

    # Add a timestamp for when the report was generated
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    date_text = f"Report Generated on: {current_time}"
    date_paragraph = Paragraph(date_text, styles['Normal'])
    elements.append(date_paragraph)

    # Add a section with risk factors or additional insights
    risk_text = "Based on your BMI and smoking status, you may fall into a higher-risk category, which could increase your insurance cost."
    risk_paragraph = Paragraph(risk_text, styles['Normal'])
    elements.append(risk_paragraph)

    # Table with data to be displayed in the PDF
    data_for_table = [
        ['Field', 'Value'],
        ['Age', str(data['age'])],
        ['Sex', data['sex']],
        ['BMI', str(data['bmi'])],
        ['Children', str(data['children'])],
        ['Smoker', data['smoker']],
        ['Region', data['region']],
        ['Predicted Insurance Cost', f"${prediction:.2f}"]
    ]

    # Create a table for the data
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
    elements.append(table)

    # Add a footer with additional info
    footer_text = "For more information, visit www.example.com"
    footer_paragraph = Paragraph(footer_text, styles['Normal'])
    elements.append(footer_paragraph)

    # Build the document
    doc.build(elements)

    # Get the value of the BytesIO buffer
    pdf_data = buffer.getvalue()
    buffer.close()

    # Return the PDF response
    response = HttpResponse(pdf_data, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=insurance_report.pdf'
    return response
