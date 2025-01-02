from django.shortcuts import render, redirect
from .models import UploadedData, AnalysisResult
from .form import UploadDataForm
import pandas as pd

def upload_data(request):
    if request.method == 'POST':
        form = UploadDataForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_data = form.save(commit=False)
            uploaded_data.save()
            # Perform data analysis
            df = pd.read_csv(uploaded_data.file.path)
            result = df.describe().to_string()
            AnalysisResult.objects.create(uploaded_data=uploaded_data, result=result)
            return render(request, 'home.html', {'form': form, 'success_message': 'Data successfully uploaded and analyzed.'})
    else:
        form = UploadDataForm()
    return render(request, 'upload_data.html', {'form': form})

def view_analysis_results(request):
    results = AnalysisResult.objects.all()
    return render(request, 'view_analysis_results.html', {'results': results})
