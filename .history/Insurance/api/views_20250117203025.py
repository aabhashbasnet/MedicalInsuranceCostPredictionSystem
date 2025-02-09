from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
import numpy as np
import joblib
import os
from .serializers import InsuranceSerializer
from .models import Insurance
import pandas as pd

# Load the pickled model
model_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'Model', 'InsuranceCostPredictor.pkl')
model = joblib.load(model_path)

# Define the feature names used during model training
FEATURE_NAMES = ['age', 'sex', 'bmi', 'children', 'smoker', 'region']

@api_view(['POST'])
def predict(request):
    if request.method == 'POST':
        # Deserialize the input data from the request
        serializer = InsuranceSerializer(data=request.data)
        if serializer.is_valid():
            try:
                # Save the input data to the database
                insurance_record = serializer.save()

                # Prepare input data for prediction
                input_data = tuple(serializer.validated_data.values())[:-1]  # Exclude 'prediction' field
                input_data_as_numpy_array = np.asarray(input_data)
                
                # Convert input data to DataFrame with feature names
                input_data_df = pd.DataFrame(input_data_as_numpy_array.reshape(1, -1), columns=FEATURE_NAMES)

                # Make a prediction using the model
                prediction = model.predict(input_data_df)[0]

                # Save the prediction along with the input data in the database
                insurance_record.prediction = prediction
                insurance_record.save()

                # Return the prediction in the response
                return Response({
                    "prediction": float(prediction),
                    "input_data": serializer.validated_data
                }, status=200)

            except Exception as e:
                # Return an error response if prediction fails
                return Response({"error": str(e)}, status=500)

        # Handle invalid serializer input
        return Response({"error": "Invalid input data", "details": serializer.errors}, status=400)
