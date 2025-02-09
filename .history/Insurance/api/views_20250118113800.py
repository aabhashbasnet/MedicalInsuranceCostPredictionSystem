
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
from reportlab.pdfgen import canvas
from io import BytesIO
@csrf_exempt
@api_view([])
def download_report(request):
    # Get the data sent from the frontend
    data = request.data  # Assuming you're using DRF

    # Create a BytesIO buffer to write the PDF
    buffer = BytesIO()

    # Create a PDF object
    p = canvas.Canvas(buffer, pagesize=letter)
    
    # Set up the PDF content
    p.drawString(100, 750, f"Age: {data['age']}")
    p.drawString(100, 735, f"Sex: {data['sex']}")
    p.drawString(100, 720, f"BMI: {data['bmi']}")
    p.drawString(100, 705, f"Children: {data['children']}")
    p.drawString(100, 690, f"Smoker: {data['smoker']}")
    p.drawString(100, 675, f"Region: {data['region']}")
    p.drawString(100, 660, f"Predicted Insurance Cost: ${data['prediction']}")

    # Save the PDF into the buffer
    p.showPage()
    p.save()

    # Get the value of the BytesIO buffer
    pdf_data = buffer.getvalue()
    buffer.close()

    # Return the PDF response
    response = HttpResponse(pdf_data, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=insurance_report.pdf'
    return response
