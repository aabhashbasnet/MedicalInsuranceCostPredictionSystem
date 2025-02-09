from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
import numpy as np
import joblib
import os
from .serializers import InsuranceSerializer
from .models import Insurance
import pandas as pd

# Load the pickled model with error handling
model_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'Model', 'InsuranceCostPredictor.pkl')
try:
    model = joblib.load(model_path)
except Exception as e:
    raise ValueError(f"Error loading model: {e}")

FEATURE_NAMES = ['age', 'sex', 'bmi', 'children', 'smoker', 'region']

@api_view(['POST'])
def predict(request):
    if request.method == 'POST':
        serializer = InsuranceSerializer(data=request.data)
        if serializer.is_valid():
            try:
                insurance_record = serializer.save()

                # Log validated input data for debugging
                print("Validated data:", serializer.validated_data)

                input_data = tuple(serializer.validated_data.values())[:-1]  # Exclude prediction field
                input_data_as_numpy_array = np.asarray(input_data)

                # Log the reshaped input data
                print("Input data for prediction:", input_data_as_numpy_array)
                input_data_df = pd.DataFrame(input_data_as_numpy_array.reshape(1, -1), columns=FEATURE_NAMES)
                print("Input DataFrame for prediction:", input_data_df)

                prediction = model.predict(input_data_df)[0]

                insurance_record.prediction = prediction
                try:
                    insurance_record.save()
                except Exception as db_error:
                    return Response({"error": f"Database save error: {db_error}"}, status=500)

                return Response({
                    "prediction": float(prediction),
                    "input_data": serializer.validated_data
                }, status=200)

            except Exception as e:
                print("Error during prediction:", str(e))
                return Response({"error": str(e)}, status=500)

        return Response({"error": "Invalid input data", "details": serializer.errors}, status=400)
