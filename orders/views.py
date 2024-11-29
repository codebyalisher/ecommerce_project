import requests
from django.shortcuts import render
from django.http import JsonResponse

FASTAPI_BASE_URL = "http://127.0.0.1:8000"

def manage_orders(request):
    user_id = request.user.id  # Assuming user is authenticated

    try:
        # Fetch orders for the user
        orders = requests.get(f"{FASTAPI_BASE_URL}/orders/{user_id}", headers={"X-API-Key": "ORDERS_API_KEY"})
        orders.raise_for_status()  # Check if request was successful
        orders_data = orders.json()
        return render(request, "admin/manage_orders.html", {"orders": orders_data})
    except requests.exceptions.RequestException as e:
        return JsonResponse({"error": f"Failed to fetch orders: {e}"}, status=400)
