from django.urls import path
from . import views

urlpatterns = [
    path('weather/', views.weather_view, name='weather_view'),
    path('stock/', views.stock_view, name='stock_view'),
]