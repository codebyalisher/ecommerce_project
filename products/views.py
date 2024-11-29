import requests
from django.shortcuts import render
from django.http import JsonResponse

FASTAPI_BASE_URL = "http://127.0.0.1:8000"  # Replace with your FastAPI URL
def fetch_products(request):
    api_key = "PRODUCTS_API_KEY"  # Replace with the actual key from FastAPI
    try:
        response = requests.get(f"{FASTAPI_BASE_URL}/products", headers={"X-API-Key": "PRODUCTS_API_KEY"})
        response.raise_for_status()  # Raise an error for HTTP codes >= 400
    except requests.exceptions.RequestException as e:
        return JsonResponse({"error": f"Failed to fetch products: {str(e)}"}, status=400)
    
    if response.status_code == 200:
        products = response.json()
        return render(request, "products.html", {"products": products})
    return JsonResponse({"error": "Failed to fetch products"}, status=400)
