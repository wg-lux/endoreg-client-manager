from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from endoreg_db.models.annotation import AnonymizedImageLabel, AnonymousImageAnnotation, DroppedName
import os
import uuid
import requests
from django.conf import settings
#from .serializers import FileUploadSerializer
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import IsAuthenticated  # Optional, for secure API access


class Result:
    def __init__(self, **entries):
        self.__dict__.update(entries)

class SaveDataView(APIView):
    def post(self, request, *args, **kwargs):
        annotation_id = request.data.get('annotation_id')
        
        try:
            annotation = AnonymousImageAnnotation.objects.get(id=annotation_id)
            annotation.processed = True
            annotation.save()

            return Response({"message": "Data saved successfully"}, status=status.HTTP_200_OK)
        except AnonymousImageAnnotation.DoesNotExist:
            return Response({"error": "Annotation not found"}, status=status.HTTP_404_NOT_FOUND)

class ValidateAndSaveView(APIView):
    def post(self, request, *args, **kwargs):
        # Receive the processed data from the processing app
        data = request.data

        try:
            # Create or retrieve the label
            label, created = AnonymizedImageLabel.objects.get_or_create(name="Default Label")

            # Save the annotation
            annotation = AnonymousImageAnnotation.objects.create(
                label=label,
                image_name=data['image_name'],
                original_image_url=data['original_image_url'],
                polyp_count=data.get('polyp_count', 0),
                comments=data.get('comments', ''),
                gender='mixed',  # Modify if necessary based on validated data
                name_image_url=data['processed_file'],
                processed=True
            )

            # Save the names
            for gender_par in data.get('gender_pars', []):
                DroppedName.objects.create(
                    annotation=annotation,
                    name=gender_par['name'],
                    gender=gender_par['gender'],
                    x=gender_par['x'],
                    y=gender_par['y'],
                    name_image_url=gender_par['image_url'],
                )

            return Response({"message": "Validation and save successful"}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# class AnonymizationRequestView(APIView):
#     # permission_classes = [IsAuthenticated]  # Optional, for secure API access

#     def post(self, request, *args, **kwargs):
#         """Handles anonymization requests by processing an uploaded file and sending results via an API request."""
#         serializer = FileUploadSerializer(data=request.data)

#         if serializer.is_valid():
#             device = request.POST.get('device', 'olympus_cv_1500')  # Device field from request
#             file = serializer.validated_data['file']  # The uploaded file
#             validation = request.POST.get('validation', 'false').lower() in ['true', '1']

#             # Save the uploaded file temporarily
#             temp_file_path = os.path.join(settings.MEDIA_ROOT, file.name)
#             with open(temp_file_path, 'wb') as temp_file:
#                 for chunk in file.chunks():
#                     temp_file.write(chunk)

#             try:
#                 # Define the path to the EAST model used for text detection
#                 east_model_path = os.path.join(settings.BASE_DIR, 'agl_anonymizer', 'models', 'frozen_east_text_detection.pb')

#                 if not os.path.exists(east_model_path):
#                     raise FileNotFoundError(f"Model file not found: {east_model_path}")

#                 # Run the main processing function
#                 if validation:
#                     output_path, stats, original_img_path = main(temp_file_path, east_path=east_model_path, device=device, validation=True)
#                     stats = Result(**stats)

#                     # Prepare the data to send to the external API
#                     data_to_send = {
#                         'image_name': os.path.basename(temp_file_path),
#                         'original_image_url': original_img_path,
#                         'polyp_count': len(stats.gender_pars),  # Counting detected elements
#                         'comments': "Generated during anonymization",
#                         'gender': stats.gender_pars,
#                         'processed_file': output_path,
#                         'gender_pars': stats.gender_pars,
#                     }

#                     # Send the data to the external API
#                     api_url = "http://127.0.0.1:8081/save_data"
#                     headers = {
#                         'Content-Type': 'application/json',
#                     }

#                     response = requests.post(api_url, json=data_to_send, headers=headers)

#                     if response.status_code != 200:
#                         raise Exception(f"Error sending data to API: {response.text}")

#                     # Prepare the response
#                     response_data = {
#                         'processed_files': [output_path],
#                         'additional_values': 'Anonymization completed and sent to API successfully',
#                         'api_response': response.json(),
#                     }
#                 else:
#                     # Processing without validation
#                     output_path = main(temp_file_path, east_path=east_model_path, device=device, validation=False)
#                     response_data = {
#                         'processed_files': [output_path],
#                         'additional_values': 'Processing completed successfully without validation'
#                     }

#                 return Response(response_data, status=status.HTTP_200_OK)

#             except Exception as e:
#                 return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#             finally:
#                 # Cleanup the temporary file
#                 if os.path.exists(temp_file_path):
#                     os.remove(temp_file_path)

#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

