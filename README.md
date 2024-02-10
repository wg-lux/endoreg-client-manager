# endoreg-client-manager
Django Webapp to run services on EndoReg Clients

## Cheat-Sheet
endoreg-import-file-mover /home/agl-admin/endoreg-client-files/import /home/endoreg-client-files/raw/data

ffmpeg -hwaccel cuda -i NINJVP_S001_S001_T016.MOV -c:v h264_nvenc -preset slow -qp 0 -c:a copy output.mp4
ffmpeg -i NINJVP_S001_S001_T016.MOV -pix_fmt yuv420p -c:v h264_nvenc -preset slow -qp 18 -c:a aac -b:a 192k output.mp4

for i in *.MOV; do
  ffmpeg -i "$i" -pix_fmt yuv420p -c:v h264_nvenc -preset slow -qp 18 -c:a aac -b:a 192k "${i%.MOV}.mp4"
done



NINJVP_S001_S001_T016.MOV


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


## Setup Poetry Django App
- if secrets are necessary, create and insert them in NixOS
    - this application requires a django secret provided at "/home/agl-admin/.config/django-secret"


## Create Encrypted Drive
Encrypting and using an external hard drive on a NixOS (a Linux distribution) involves several steps, including formatting the drive, encrypting it, and then mounting it for use. Here's a general guide:

### 1. Identify the Drive
First, you need to identify the external hard drive's device name.

- Connect the external hard drive to your NixOS machine.
- Open a terminal and run the following command to list all connected storage devices:
  ```bash
  lsblk
  ```
- Identify your external hard drive from the list (e.g., `/dev/sdx`).

### 2. Format the Drive (Optional)
If the drive is new or you want to erase its current content, you'll need to format it. **Warning: This will erase all data on the drive.**

- Use the `fdisk` or `parted` command to create a new partition.
- Example with `fdisk`:
  ```bash
  sudo fdisk /dev/sdx
  ```

### 3. Install Cryptsetup
Ensure you have `cryptsetup` installed, as it's required for the next steps.

- Install `cryptsetup` in temporary shell:
  ```bash
  nix-shell cryptsetup
  ```

### 4. Encrypt the Drive
You'll use LUKS (Linux Unified Key Setup) for encryption.
(assuming drive is "/dev/sda")
- Encrypt the partition:
  ```bash
  sudo cryptsetup luksFormat /dev/sda1
  ```
- Open the encrypted partition:
  ```bash
  sudo cryptsetup open /dev/sdx1 endoreg-sensitive-data
  ```

### 5. Create a Filesystem
Now, create a filesystem on the encrypted partition.

- Common choices are ext4, NTFS, or FAT32. For Linux systems, ext4 is typical:
  ```bash
  sudo mkfs.ext4 /dev/mapper/endoreg-sensitive-data
  ```

### 6. Mount the Drive
Mount the drive to use it.

- Create a mount point:
  ```bash
  sudo mkdir /mnt/endoreg-sensitive-data
  ```
- Mount the encrypted drive:
  ```bash
  sudo mount /dev/mapper/endoreg-sensitive-data /mnt/endoreg-sensitive-data
  ```

### 7. Using the Drive
Now the drive is ready to use. You can access it via `/mnt/endoreg-sensitive-data`.

### 8. Unmounting and Closing
When finished, unmount and close the encrypted drive:

- Unmount the drive:
  ```bash
  sudo umount /mnt/agl-hdd-01
  ```
- Close the encrypted partition:
  ```bash
  sudo cryptsetup close agl-hdd-01
  ```

### Important Notes
- Always back up important data before proceeding with formatting or encryption.
- Ensure that your kernel supports the encryption method you choose.
- Remember the encryption passphrase; losing it means losing access to the data on the drive.
- This process can be automated or integrated into system services for ease of use.

This guide is intended for users with a good understanding of Linux systems. If you're new to these concepts, consider seeking additional detailed guides or assistance.
