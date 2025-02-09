
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
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from io import BytesIO
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view

@csrf_exempt
@api_view(['POST'])
def download_report(request):
    # Get the data sent from the frontend
    data = request.data  # Assuming you're using DRF
    
    # Ensure prediction is a float (in case it's passed as a string)
    prediction = float(data['prediction']) if isinstance(data['prediction'], str) else data['prediction']
    
    # Create a BytesIO buffer to write the PDF
    buffer = BytesIO()

    # Create a SimpleDocTemplate to generate the PDF document
    doc = SimpleDocTemplate(buffer, pagesize=letter)

    # Table data
    table_data = [
        ['Field', 'Value'],  # Table headers
        ['Age', str(data['age'])],
        ['Sex', data['sex']],
        ['BMI', str(data['bmi'])],
        ['Children', str(data['children'])],
        ['Smoker', data['smoker']],
        ['Region', data['region']],
        ['Predicted Insurance Cost', f"${prediction:.2f}"]  # Format prediction as a float
    ]

    # Create a Table
    table = Table(table_data)

    # Apply TableStyle for better formatting
    table.setStyle(TableStyle([
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),  # White text for headers
        ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),  # Dark blue background for headers
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # Center-align all cells
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),  # Bold font for headers
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),  # Regular font for the rest
        ('FONTSIZE', (0, 0), (-1, -1), 10),  # Font size for all cells
        ('GRID', (0, 0), (-1, -1), 1, colors.black),  # Black grid lines
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),  # Padding for the header row
        ('TOPPADDING', (0, 1), (-1, -1), 10),  # Padding for the content rows
        ('LEFTPADDING', (0, 0), (-1, -1), 8),  # Padding for left side of cells
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),  # Padding for right side of cells
    ]))

    # Build the PDF document with the table
    doc.build([table])

    # Get the value of the BytesIO buffer
    pdf_data = buffer.getvalue()
    buffer.close()

    # Return the PDF response
    response = HttpResponse(pdf_data, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=insurance_report.pdf'
    return response
