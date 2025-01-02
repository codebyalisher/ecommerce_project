from django.db import models

class UploadedData(models.Model):
    file = models.FileField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

class AnalysisResult(models.Model):
    uploaded_data = models.ForeignKey(UploadedData, on_delete=models.CASCADE)
    result = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)