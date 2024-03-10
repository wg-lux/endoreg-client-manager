# endoreg-client-manager
Django Webapp to run services on EndoReg Clients

## Initial Setup
- Create Superuser: `python manage.py shell"
- manual migrations (?)
  - python manage.py migrate django_celery_results
  - python manage.py migrate data_collector

## TMP
`python -m celery -A endoreg_client_manager worker -l info` # -E would add task monitoring

## Cheat-Sheet
endoreg-import-file-mover /home/agl-admin/endoreg-client-files/import /home/endoreg-client-files/raw/data

ffmpeg -hwaccel cuda -i NINJVP_S001_S001_T016.MOV -c:v h264_nvenc -preset slow -qp 0 -c:a copy output.mp4
ffmpeg -i NINJVP_S001_S001_T016.MOV -pix_fmt yuv420p -c:v h264_nvenc -preset slow -qp 18 -c:a aac -b:a 192k output.mp4

for i in *.MOV; do
  ffmpeg -i "$i" -pix_fmt yuv420p -c:v h264_nvenc -preset slow -qp 18 -c:a aac -b:a 192k "${i%.MOV}.mp4"
done

## Configuration
currently some environment variables are set in endoreg_client_manger/.env #FIXME

## Scheduled tasks
We use Cerlery for that. Main configuration is located in the same folder as settings.py (./endoreg_client_manager/endoreg_client_manager/celery.py)

To schedule tasks, "django_celery_beat" must be added to INSTALLED_APPS

make sure that celery beat is running, we do this in our flake.nix

### Scheduling new tasks:
1. Generate an empty migration file in one of your apps (e.g., data_collector):
'python manage.py makemigrations data_collector --empty --name schedule_move_files_task'

2. In the migration, we nee to reference 
- the currently latest migration of the app in which the task is defined which is just the one before the currently created one
- the currently latest migration of django_celery_beat which we can find out by running: ''

## Static Files
We host staticfiles using whitenoise: https://whitenoise.readthedocs.io/en/latest/django.html

# Devlog
## 2024-03-10 Debugging RawVideofile

/mnt/hdd-sensitive/Pseudo/import/video/e2a73bd9-fe4a-4608-a451-b19a609001d5.mp4

video = RawVideoFile.objects.get()

from endoreg_db.models import RawVideoFile
from pathlib import Path
video = RawVideoFile.objects.get()
video.update_text_metadata()

fp = Path("/mnt/hdd-sensitive/Pseudo/import/video/8ac93c6f-68f9-42b8-ab84-f9d0e5835df1.mp4")
pd = Path("/mnt/hdd-sensitive/Pseudo/import/video/")
frame_dir = Path("/home/agl-admin/endoreg-client-manager/endoreg_client_manager/data/tmp/raw_frames")
video = RawVideoFile.create_from_file(fp,pd, center_name = "university_hospital_wuerzburg", processor_name = "olympus_cv_1500", frame_dir_parent=frame_dir)


## OCR

from endoreg_db.models import RawVideoFile
from pathlib import Path

fn = "1e959443-69b1-4004-bd5a-3431f2a16d7f.mp4"
fp = Path(f"/mnt/hdd-sensitive/DropOff/data/{fn}")
pd = Path("/mnt/hdd-sensitive/Pseudo/import/video/")
frame_dir = Path("/home/agl-admin/endoreg-client-manager/")
center_name = "university_hospital_wuerzburg"
processor_name = "olympus_cv_1500"

vid = RawVideoFile.create_from_file(
  file_path = fp,
  video_dir_parent = pd,
  center_name = center_name,
  processor_name = processor_name,
  frame_dir_parent = frame_dir,
)

