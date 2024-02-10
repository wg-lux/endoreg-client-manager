from django.db import models

# RawFile model
class RawFile(models.Model):
    file = models.FileField(upload_to='raw_data/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file.name
