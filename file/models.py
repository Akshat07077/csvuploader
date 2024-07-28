from django.db import models

from django.contrib.auth.models import User

class CSVfiles(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to="csv/")
    uploaded_at = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return self.file.name

class CSVData(models.Model):
    file = models.ForeignKey(CSVfiles, related_name='rows', on_delete=models.CASCADE)
    row_number = models.IntegerField()
    data = models.JSONField() 