from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from orders.models import Order  # Correct import for Order and Cart models from orders.models
from .schemas import OrderCreate, Order  # FastAPI schemas for validation and serialization
from .database import get_db
from typing import List
from users.models import Userm  # Import the User model from users.models


router = APIRouter()

# Create an order
@router.post("/orders", response_model=Order)
def create_order(order: OrderCreate, db: Session = Depends(get_db)):
    # Fetch the user from Django ORM
    try:
        user =Userm.objects.get(id=order.user_id)
    except Userm.DoesNotExist:
        raise HTTPException(status_code=404, detail="User not found")

    # Create order
    db_order = Order(user=user, total_price=order.total_price, status=order.status)
    db_order.save()  # Save the order

    # Set products in the order using ManyToMany relationship
    db_order.products.set(order.product_ids)
    db_order.calculate_total()  # Recalculate the total price of the order based on products

    return db_order

# Get all orders for a user
@router.get("/orders/{user_id}", response_model=List[Order])
def get_orders(user_id: int, db: Session = Depends(get_db)):
    orders = Order.objects.filter(user_id=user_id)
    return orders

# Get a specific order by ID
@router.get("/orders/{order_id}", response_model=Order)
def get_order(order_id: int, db: Session = Depends(get_db)):
    try:
        order = Order.objects.get(id=order_id)
    except Order.DoesNotExist:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


