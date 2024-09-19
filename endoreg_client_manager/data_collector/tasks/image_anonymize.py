from pathlib import Path
import os
import requests
from celery import shared_task
from django.conf import settings
from .common import single_instance_task, LOCK_EXPIRE
from endoreg_db.models import AnonymousImageAnnotation, AnonymizedImageLabel, Name

@shared_task(bind=True)
@single_instance_task(lock_expire=LOCK_EXPIRE)
def task_anonymize_files(self, image_path):
    try:
        """Anonymize files and save annotations and names to the database"""

        # Ensure the file exists
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"No such file or directory: '{image_path}'")

        # Define the URL of the Django API endpoint for anonymization
        api_url = 'http://127.0.0.1:8080/process-file/'

        # Open the file in binary mode and send it as part of the multipart form-data payload
        with open(image_path, 'rb') as image_file:
            files = {
                'file': image_file,
            }
            data = {
                'title': 'Example Image',
                'device': 'olympus_cv_1500',  # Add the device parameter here
                'validation': True
            }
            response = requests.post(api_url, files=files, data=data)

        # Check if the response from the API was successful
        if response.status_code != 200:
            raise Exception(f"Failed to process image: {response.text}")

        response_data = response.json()

        # Extract required data from the response
        processed_files = response_data.get('processed_files', [])
        gender_pars = response_data.get('gender', [])  # Changed from 'gender_pars' to 'gender'
        original_image_path = response_data.get('original_image_url', '')

        # Save the results to the database
        try:
            # Create or get the label for the annotation
            label, created = AnonymizedImageLabel.objects.get_or_create(name="Default Label")

            # Create the image annotation
            annotation = AnonymousImageAnnotation.objects.create(
                label=label,
                image_name=os.path.basename(image_path),
                original_image_url=original_image_path,
                polyp_count=len(gender_pars),
                comments="Automatically generated annotation",
                gender="neutral",  
                name_image_url=processed_files[0] if processed_files else '',
                processed=True
            )

            for gender_par in gender_pars:
                Name.objects.create(
                    annotation=annotation,
                    name=gender_par['name'],
                    gender=gender_par['gender'],
                    x=gender_par['x'],
                    y=gender_par['y'],
                    name_image_url=gender_par['image_url'],
                    box_coordinates=gender_par.get('box_coordinates', '')  # Optionally save box coordinates if available
                )

            print(f"Annotation and names saved successfully for image: {image_path}")

        except Exception as e:
            raise Exception(f"Failed to save annotation and names: {str(e)}")
    except Exception as exc:
        self.retry(exc=exc)
