from pydantic import BaseModel, EmailStr
from typing import List, Optional
from decimal import Decimal
from datetime import datetime



class RoleBase(BaseModel):
    """Schema for roles."""
    name: str

    class Config:
        orm_mode = True


class RoleCreate(RoleBase):
    pass


# Validate that passwords match
    def validate_password(self):
        if self.password != self.confirm_password:
            raise ValueError("Passwords do not match")


# fastapi/schemas.py
class UserEmail(BaseModel):
    email: str
class UserCreate(BaseModel):
    email: EmailStr
    password: str
    confirm_password: str

class LoginResponse(BaseModel):
    message: str
    token: str

# Define a request model
class LoginRequest(BaseModel):
    email: str
    password: str

class KeyGenerationResponse(BaseModel):
    api_key: str
    expires_at: datetime

class UserResponse(BaseModel):
    email: EmailStr
    role: str
    is_active: bool

# Pydantic model for OTP request
class OTPRequest(BaseModel):
    email: str  # or phone number depending on your use case

class OTPVerification(BaseModel):
    email: str  # or phone number
    otp: str

# fastapi/schemas.py

class ProductBase(BaseModel): 
    title: str
    description: str
    price: Decimal
    category: str

class ProductCreate(ProductBase):
    pass

class Product(ProductBase):
    id: int
    image_url: str  # You might need to create the full URL here if needed

    class Config:
        orm_mode = True


class CartBase(BaseModel):
    user_id: int
    product_ids: List[int]  # Represent the list of product IDs in the cart

    class Config:
        orm_mode = True  # Tells Pydantic to convert from Django model to Pydantic model

class Cart(CartBase):
    id: int
    total_price: Decimal
    products: List[Product]  # Serialize products in the cart

    class Config:
        orm_mode = True 



class OrderBase(BaseModel):
    user_id: int
    product_ids: List[int]
    total_price: float

    class Config:
        orm_mode = True

class OrderCreate(OrderBase):
    status: str  # "Pending" or "Shipped"

class Order(OrderBase):
    id: int
    status: str

    class Config:
        orm_mode = True

