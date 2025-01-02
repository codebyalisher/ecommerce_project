import os
import django
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from fastapi import FastAPI, Request
import logging
import time
from django.conf import settings


# Set the Django settings module before any other imports
os.environ['DJANGO_SETTINGS_MODULE'] = 'ecommerce_project.settings'
# Initialize Django settings
django.setup()

# Now import the routers after Django setup
from .user_api import router as user_router  # Import user API
from .task_manager_api import router as task_manager_router  # Import task manager API
from .order_api import router as order_router  # Import order API
from .products_api import router as product_router  # Import order API

from users.models import APIKey
from fastapi import  HTTPException
from asgiref.sync import sync_to_async
from django.utils import timezone
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

# Configure logging
logging.basicConfig(level=logging.INFO,format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("error.log"),
        logging.StreamHandler()
    ])
logger = logging.getLogger(__name__)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    idem = f"{time.time()}"
    logger.info(f"rid={idem} start request path={request.url.path}")
    start_time = time.time()

    response = await call_next(request)

    process_time = time.time() - start_time
    formatted_process_time = '{0:.2f}'.format(process_time * 1000)
    logger.info(f"rid={idem} completed_in={formatted_process_time}ms status_code={response.status_code}")

    return response

'''@app.middleware("http")
async def api_key_validator(request: Request, call_next):
    api_key = request.headers.get("X-API-KEY")
    if not api_key:
        logger.error("API Key required")
        raise HTTPException(status_code=403, detail="API Key required")
    
    try:
        logger.info(f"Checking API Key: {api_key}")
        db_api_key = await sync_to_async(APIKey.objects.get)(key=api_key)
        if db_api_key.expires_at < timezone.now():
            logger.error(f"Expired API Key: {api_key}")
            raise HTTPException(status_code=403, detail="API Key expired")
        logger.info(f"API Key is valid: {api_key}")
    except APIKey.DoesNotExist:
        logger.error(f"Invalid API Key: {api_key}")
        raise HTTPException(status_code=403, detail="Invalid API Key")
    
    response = await call_next(request)
    return response'''

# Include the routers for different apps (user, order)
app.include_router(user_router, prefix="/users", tags=["users"])
app.include_router(task_manager_router, prefix="/tasks", tags=["tasks"])
app.include_router(order_router, prefix="/orders", tags=["orders"])
app.include_router(product_router, prefix="/products", tags=["products"])
