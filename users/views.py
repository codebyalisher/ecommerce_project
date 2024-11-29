# Define the URL for your FastAPI signup endpoint
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login,logout
from django.contrib.sessions.models import Session
from django.http import HttpResponse,JsonResponse
import requests
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def form(request, action=None):  # Accept `action` as a parameter
    if action is None:
        return HttpResponse("Invalid action", status=400)

    form_action = action  # 'signup' or 'signin'
    fastapi_url = f"http://127.0.0.1:8000/users/{form_action}/"
    error_message = None 

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        if form_action == 'signup':
            confirm_password = request.POST.get('confirm_password')
            if password != confirm_password:                
                error_message = f"Password do not match, status={response.status_code}"                    

            # Direct POST to FastAPI without redundant GET request
            response = requests.post(
                fastapi_url,
                json={
                    'email': email,
                    'password': password,
                    'confirm_password': confirm_password,
                },
                headers={'Content-Type': 'application/json'}
            )

            if response.status_code == 400:
                # Handle specific error messages from FastAPI
                error_message = response.json().get('detail', 'Signup failed')
                if error_message == "Email already registered":
                    error_message = f"Email already registered status={response.status_code}"                    
                return HttpResponse(error_message, status=response.status_code)
            elif response.status_code == 200:
                return redirect('login')
            else:                                
                error_message = f"An unexpected error occurred status={response.status_code}"

        if form_action == 'login':
            response = requests.post(
                fastapi_url,
                json={
                    'email': email,
                    'password': password,
                },
                headers={'Content-Type': 'application/json'}
            )            

            if response.status_code == 200:
                response_json = response.json()
                token = response_json.get('token')                
                if token:
                    request.session['access_token'] = token #we are storing the token in session for later use
                    return render(request,'otp.html', {'response': response_json})
                else:
                    error_message =f"No access token received,status={response.status_code} "
            else:
                error_message = response.json().get('detail', 'Login failed')
                
        if form_action == 'logout':
            # Clear session tokens
            if 'access_token' in request.session:
                del request.session['access_token']
            if 'refresh_token' in request.session:
                del request.session['refresh_token']            
            # Delete the sessionid cookie
            response = redirect('login')  # Redirect to login page
            response.delete_cookie('sessionid')  # Explicitly delete the session cookie
            return response
        return HttpResponse("Logout successful", status=200)
        
        if form_action=='refresh':
            refresh_token = request.session.get('refresh_token')
            if not refresh_token:
                return JsonResponse({'detail': 'No refresh token found. Please log in again.'}, status=401)
            # Make a request to FastAPI to refresh the access token
            response = requests.post(
                fastapi_url,
                json={'refresh_token': refresh_token},
                headers={'Content-Type': 'application/json'}
            )
            if response.status_code == 200:
                # FastAPI has issued a new access token
                data = response.json()
                new_access_token = data.get('access_token')
                
                # Update the session with the new access token
                request.session['access_token'] = new_access_token
                
                return JsonResponse({'access_token': new_access_token}, status=200)
            else:
                # Handle token refresh failure
                return JsonResponse(response.json(), status=response.status_code)

    return render(request, 'form.html', {'form_action': form_action,'error':error_message})

    subject = 'Your OTP Code'
    message = f'Your OTP code is: {otp}'
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])

# Send OTP via SMS (using Twilio as an example)
'''def send_otp_sms(user, otp):
    account_sid = settings.TWILIO_ACCOUNT_SID
    auth_token = settings.TWILIO_AUTH_TOKEN
    client = Client(account_sid, auth_token)
    
    message = client.messages.create(
        body=f'Your OTP code is: {otp}',
        from_=settings.TWILIO_PHONE_NUMBER,
        to=user.phone_number  # Assuming user has a `phone_number` field
    )'''

@csrf_exempt
def otp_form(request, action):
    fastapi_url = f"http://127.0.0.1:8000/users/{action.replace('_', '-')}/"
    if action == 'generate_otp':
        if request.method == 'POST':
            email = request.POST.get('email')
            if not email:
                return JsonResponse({'error': 'Email is required'}, status=400)
            # Call the FastAPI endpoint
            response = requests.post(fastapi_url, json={'email': email})
            if response.status_code == 200:
                return JsonResponse({'message': 'OTP sent successfully,see your email'}, status=200)
            else:
                return JsonResponse(response.json(), status=response.status_code)

    elif action == 'verify_otp':
        if request.method == 'POST':
            email = request.POST.get('email')
            otp = request.POST.get('otp')
            if not email or not otp:
                return JsonResponse({'error': 'Email and OTP are required'}, status=400)
            # Call the FastAPI endpoint
            response = requests.post(fastapi_url, json={'email': email, 'otp': otp})
            if response.status_code == 200:
                response_data={'message': 'OTP verified successfully','email':email}
                return render(request, 'home.html', {'response': response_data})                         
            else:
                return JsonResponse(response.json(), status=response.status_code)
    return HttpResponse("Invalid action", status=400)

def home(request):
    return render(request, 'home.html')

import jwt
def dashboard_view(request):
    token = request.session.get("jwt_token")
    if not token:
        return redirect("login")
    
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        role = payload["role"]
        
        if role == "admin":
            return render(request, "admin_dashboard.html")
        elif role == "authority":
            return render(request, "authority_dashboard.html")
        else:
            return render(request, "user_dashboard.html")
    except jwt.ExpiredSignatureError:
        return redirect("login")


def manage_roles(request):
    if request.method == "POST":
        # Handle role creation or assignment
        pass
    roles = Role.objects.all()
    return render(request, "manage_roles.html", {"roles": roles})


def manage_products(request):
    if request.method == "POST":
        # Create or update a product via FastAPI
        product_data = {
            "name": request.POST["name"],
            "description": request.POST["description"],
            "price": request.POST["price"],
            "category_id": request.POST["category_id"]
        }
        api_key = "PRODUCTS_API_KEY"
        response = requests.post(f"{FASTAPI_BASE_URL}/products", json=product_data, headers={"X-API-Key": api_key})
        if response.status_code == 200:
            return redirect("admin_dashboard")  # Redirect to admin dashboard
        else:
            return JsonResponse({"error": "Failed to create product"}, status=400)

    products = requests.get(f"{FASTAPI_BASE_URL}/products", headers={"X-API-Key": "PRODUCTS_API_KEY"})
    return render(request, "admin/manage_products.html", {"products": products.json()})


def user_dashboard(request):
    # Fetch products
    products = requests.get(f"{FASTAPI_BASE_URL}/products", headers={"X-API-Key": "PRODUCTS_API_KEY"})
    if products.status_code == 200:
        products_data = products.json()
    
    # Fetch orders for the user
    orders = requests.get(f"{FASTAPI_BASE_URL}/orders/{user_id}", headers={"X-API-Key": "ORDERS_API_KEY"})
    if orders.status_code == 200:
        orders_data = orders.json()

    return render(request, "user/dashboard.html", {
        "products": products_data,
        "orders": orders_data
    })


def validate_api_key(api_key: str) -> bool:
    """
    Validates the API Key by checking if it exists and is not expired.
    """
    try:
        raw_key = base64.urlsafe_b64decode(api_key).decode()
        api_key_obj = APIKey.objects.get(key=raw_key)
        if api_key_obj.is_valid():
            return True
        else:
            raise HTTPException(status_code=401, detail="API key expired")
    except APIKey.DoesNotExist:
        raise HTTPException(status_code=401, detail="Invalid API key")
