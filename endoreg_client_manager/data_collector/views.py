# data_collector/views.py

from django.shortcuts import redirect
from django.urls import reverse
from .tasks import mount_partition, unmount_partition, is_mountpoint
from django.http import JsonResponse
from django.conf import settings
from rest_framework.views import APIView
from .serializers import AnonymizedFileSerializer, AnonymousImageAnnotationSerializer, RawFileSerializer, ValidateAndSaveSerializer
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated  # Optional
from endoreg_db.models import AnonymizedFile, AnonymousImageAnnotation

def mount_partition_view(request, partition_name):
    mount_partition.delay(partition_name)
    return JsonResponse({"status": f"Mounting initiated for {partition_name}"})

def unmount_partition_view(request, partition_name):
    unmount_partition.delay(partition_name)
    return JsonResponse({"status": f"Unmounting initiated for {partition_name}"})

def check_mount_status(request):
    mount_status = {}
    for partition_name, partition_info in settings.PARTITION_DICT.items():
        try:
            mounted = is_mountpoint.delay(partition_info['path'].resolve().as_posix()).get(timeout=10)
            mount_status[partition_name] = mounted
        except Exception as e:
            mount_status[partition_name] = str(e)
    return JsonResponse(mount_status)

# data_collector/views.py

from rest_framework.views import APIView
from rest_framework.response import Response
import logging

logger = logging.getLogger(__name__)

class ValidateAndSaveView(APIView):
    # Uncomment and adjust permissions as needed
    # permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = ValidateAndSaveSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            try:
                # Save AnonymizedFile
                anonymized_file = AnonymizedFile.objects.create(
                    image_name=data['image_name'],
                    original_image_url=data.get('original_image_url', ''),
                    polyp_count=data['polyp_count'],
                    comments=data.get('comments', ''),
                    name_image_url=data['name_image_url']
                )

                # Save AnonymousImageAnnotation and related Name entries
                for gender_par in data.get('gender', []):
                    name = gender_par.get('name', 'Unknown')
                    gender = gender_par.get('gender', 'Unknown')
                    x = gender_par.get('x', 0)
                    y = gender_par.get('y', 0)
                    image_url = gender_par.get('image_url', '')
                    box_coordinates = gender_par.get('box_coordinates', '')

                    # Assuming 'label' is related to the annotation
                    # Adjust according to your actual model relationships
                    label_name = gender_par.get('label_name', 'Default Label')
                    label, created = AnonymizedImageLabel.objects.get_or_create(name=label_name)

                    annotation = AnonymousImageAnnotation.objects.create(
                        label=label,
                        image_name=data['image_name'],
                        original_image_url=data.get('original_image_url', ''),
                        polyp_count=data['polyp_count'],
                        comments=data.get('comments', ''),
                        gender=gender,
                        name_image_url=image_url,
                        processed=True
                    )

                    # Save Name entries related to the annotation
                    Name.objects.create(
                        annotation=annotation,
                        name=name,
                        gender=gender,
                        x=x,
                        y=y,
                        name_image_url=image_url,
                        box_coordinates=box_coordinates
                    )

                logger.info(f"Data saved successfully for image: {data['image_name']}")
                return Response({"message": "Data saved successfully"}, status=status.HTTP_201_CREATED)

            except Exception as e:
                logger.error(f"Error saving data: {e}")
                return Response({"error": "Failed to save data"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            logger.warning(f"Validation failed: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SaveData(APIView):
    #permission_classes = [IsAuthenticated]  # Optional

    def post(self, request):
        serializer = AnonymizedFileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({"status": "Data saved successfully"}, status=201)
        else:
            return JsonResponse(serializer.errors, status=400)

class AnonymizedFileListCreate(generics.ListCreateAPIView):
    queryset = AnonymizedFile.objects.all()
    serializer_class = AnonymizedFileSerializer
    #permission_classes = [IsAuthenticated]  # Optional
    
# data_collector/views.py

from .serializers import AnonymousImageAnnotationSerializer

class AnnotationListCreate(generics.ListCreateAPIView):
    queryset = AnonymousImageAnnotation.objects.all()
    serializer_class = AnonymousImageAnnotationSerializer
    permission_classes = [IsAuthenticated]  # Optional

class ProcessFileView(APIView):
    # permission_classes = [IsAuthenticated]  # Optional

    def post(self, request, *args, **kwargs):
        serializer = FileUploadSerializer(data=request.data)

        if serializer.is_valid():
            device = request.POST.get('device', 'olympus_cv_1500')
            file = serializer.validated_data['file']
            validation = request.POST.get('validation', 'false').lower() in ['true', '1']

            # Save the uploaded file to a temporary location
            temp_file_path = os.path.join(settings.MEDIA_ROOT, file.name)
            with open(temp_file_path, 'wb') as temp_file:
                for chunk in file.chunks():
                    temp_file.write(chunk)

            try:
                # Get the path to the EAST model
                east_model_path = os.path.join(settings.BASE_DIR, 'agl_anonymizer', 'models', 'frozen_east_text_detection.pb')
                if not os.path.exists(east_model_path):
                    raise FileNotFoundError(f"Model file not found: {east_model_path}")

                # Call the main processing function
                output_path, stats, original_img_path = main(temp_file_path, east_path=east_model_path, device=device, validation=validation)

                # Prepare the data to be sent to the endoreg client manager
                data_to_send = {
                    'image_name': os.path.basename(temp_file_path),
                    'original_image_url': original_img_path,
                    'polyp_count': len(stats.gender_pars),
                    'comments': "Generated during anonymization",
                    'gender': stats.gender_pars,  # Adjust if needed
                    'name_image_url': output_path,
                    # Add other fields as necessary
                }

                # Send data to the endoreg client manager for saving
                api_url = "http://127.0.0.1:8001/validate-and-save/"  # The endpoint in the endoreg client manager
                headers = {'Content-Type': 'application/json'}
                response = requests.post(api_url, json=data_to_send, headers=headers)

                if response.status_code != 200:
                    raise Exception(f"Error sending data to client manager: {response.text}")

                return JsonResponse({
                    'status': 'success',
                    'message': 'Processing completed and data sent to endoreg client manager',
                    'api_response': response.json(),
                }, status=status.HTTP_200_OK)

            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            finally:
                if os.path.exists(temp_file_path):
                    os.remove(temp_file_path)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class HandleAnnotationView(APIView):
    def post(self, request, *args, **kwargs):
        # Extract data from the request
        annotation_data = request.data.get('annotation')

        if not annotation_data:
            return Response({"error": "No annotation data provided"}, status=status.HTTP_400_BAD_REQUEST)

        # Process the annotation data, e.g., save to database
        label, created = AnonymizedImageLabel.objects.get_or_create(name=annotation_data['label_name'])
        annotation = AnonymousImageAnnotation.objects.create(
            label=label,
            image_name=annotation_data['image_name'],
            original_image_url=annotation_data['original_image_url'],
            polyp_count=annotation_data.get('polyp_count', 0),
            comments=annotation_data.get('comments', ''),
            gender=annotation_data.get('gender', 'unknown'),
            name_image_url=annotation_data.get('name_image_url', ''),
            processed=True
        )

        return Response({"message": "Annotation saved successfully"}, status=status.HTTP_200_OK)
