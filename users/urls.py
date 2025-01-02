# urls.py (Django)

from django.urls import path
from . import views 

urlpatterns = [
    path('signup/', views.form, {'action': 'signup'}, name='signup'),
    path('', views.form, {'action': 'signup'}, name='signup'),  #this is being set as when the application will be loaded
    path('login/', views.form, {'action': 'login'}, name='login'),
    path('logout/', views.form,{'action':'logout'}, name='logout'),
    path('refresh_token/', views.form,{'action':'refresh'}, name='refresh_token'),
    path('generate-otp/', views.otp_form, {'action': 'generate_otp'}, name='generate_otp'),
    path('verify-otp/', views.otp_form, {'action': 'verify_otp'}, name='verify_otp'),
    path('home/', views.home, name='home'),
]
