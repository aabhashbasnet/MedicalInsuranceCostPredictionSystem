# from django.shortcuts import render
# from rest_framework.decorators import api_view
# from rest_framework.response import Response
# import numpy as np
# import joblib
# import os
# from .serializers import InsuranceSerializer

# # Get the path to the pickled model file
# model_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'Model', 'InsuranceCostPredictor.pkl')

# # Load the pickled model
# model = joblib.load(model_path)

# @api_view(['POST'])
# def predict(request):
#     if request.method == 'POST':
#         # Deserialize the input data from the request
#         serializer = InsuranceSerializer(data=request.data)
        
#         if serializer.is_valid():
#             # Convert input data to the input format for the model
#             input_data = tuple(serializer.validated_data.values())
#             input_data_as_numpy_array = np.asarray(input_data)
#             input_data_reshaped = input_data_as_numpy_array.reshape(1, -1)
            
#             # Print to check if the reshaping is correct
#             print(input_data_reshaped)
            
#             # Make a prediction using the model
#             prediction = model.predict(input_data_reshaped)
            
#             # Return the prediction as a JSON response (ensure it's in the correct format)
#             return Response({"prediction": prediction[0]})
#         else:
#             # Return an error response if the serializer is invalid
#             return Response({"error": "Invalid input data"}, status=400)
