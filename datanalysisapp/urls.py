from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.upload_data, name='upload_data'),
    path('results/', views.view_analysis_results, name='view_analysis_results'),
]