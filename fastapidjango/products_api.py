from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from .database import get_db
from fastapi.params import Query
from typing import List
from products.models import Product, Cart  # Correct import for Product and Cart models from products.models
from .schemas import ProductBase,ProductCreate, Product, CartBase,Cart  # FastAPI schemas for validation and serialization

router = APIRouter()

# Create a product
@router.post("/products", response_model=Product)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    db_product = Product.objects.create(
        title=product.title, 
        description=product.description, 
        price=product.price, 
        category=product.category
    )
    db_product.save()
    return db_product

# Search for products
@router.get("/products/search", response_model=List[Product])
async def search_products(query: str = Query(..., min_length=3), db: Session = Depends(get_db)):
    products = Product.objects.filter(title__icontains=query)
    return products

# Read all products
@router.get("/products", response_model=List[Product])
def get_products(db: Session = Depends(get_db)):
    products = Product.objects.all()
    return products

# Read a single product
@router.get("/products/{product_id}", response_model=Product)
def get_product(product_id: int, db: Session = Depends(get_db)):
    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

# Update a product
@router.put("/products/{product_id}", response_model=Product)
def update_product(product_id: int, product: ProductCreate, db: Session = Depends(get_db)):
    try:
        db_product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        raise HTTPException(status_code=404, detail="Product not found")
    
    db_product.title = product.title
    db_product.description = product.description
    db_product.price = product.price
    db_product.category = product.category
    db_product.save()
    return db_product

# Delete a product
@router.delete("/products/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    try:
        db_product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        raise HTTPException(status_code=404, detail="Product not found")
    
    db_product.delete()
    return {"message": "Product deleted successfully"}

# Cart routes: Add products to the user's cart
@router.post("/cart/add", response_model=Cart)
async def add_to_cart(cart: CartBase, db: Session = Depends(get_db)):
    # Retrieve or create a cart for the user
    user_cart, created = Cart.objects.get_or_create(user_id=cart.user_id)
    
    # Add products to the cart
    for product_id in cart.product_ids:
        try:
            product = Product.objects.get(id=product_id)
            user_cart.products.add(product)  # Add product to the cart (ManyToMany)
        except Product.DoesNotExist:
            raise HTTPException(status_code=404, detail=f"Product with id {product_id} not found")
    
    user_cart.update_total()  # Update the cart total price based on added products
    return user_cart
