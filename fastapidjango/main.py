import os
import django
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from fastapi import FastAPI
from django.conf import settings
# Set the Django settings module before any other imports
os.environ['DJANGO_SETTINGS_MODULE'] = 'ecommerce_project.settings'
# Initialize Django settings
django.setup()

# Now import the routers after Django setup
from .user_api import router as user_router  # Import user API
from .order_api import router as order_router  # Import order API
from .products_api import router as product_router  # Import order API
# Initialize FastAPI app
app = FastAPI()
SECRET_KEY = settings.SECRET_KEY

app.add_middleware(
    SessionMiddleware,
    secret_key=SECRET_KEY,  # Ensure SECRET_KEY is a string
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust for your allowed domains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the routers for different apps (user, order)
app.include_router(user_router, prefix="/users", tags=["users"])
app.include_router(order_router, prefix="/orders", tags=["orders"])
app.include_router(product_router, prefix="/products", tags=["products"])
