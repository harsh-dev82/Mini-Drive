from django.db import models
from django.contrib.auth.models import User

class UploadedFile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # which user uploaded
    file = models.FileField(upload_to='uploads/')            # store file in media/uploads/
    uploaded_at = models.DateTimeField(auto_now_add=True)    # upload timestamp

    def __str__(self):
        return f"{self.user.username} - {self.file.name}"
