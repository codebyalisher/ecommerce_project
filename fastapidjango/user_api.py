from fastapi import APIRouter, HTTPException, Response, Request
from passlib.hash import bcrypt
from passlib.context import CryptContext
from passlib.exc import UnknownHashError 
from django.conf import settings
from users.models import Userm, APIKey
from .schemas import UserEmail,UserCreate, LoginResponse, KeyGenerationResponse, UserResponse,LoginRequest,OTPRequest,OTPVerification
from datetime import datetime, timedelta
from asgiref.sync import sync_to_async
from fastapi.responses import RedirectResponse
import jwt
import uuid
import base64
from dotenv import load_dotenv
load_dotenv()


router = APIRouter()

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = "HS256"

# Helper Functions
# Helper function to create a JWT token
def create_jwt_token(email: str, expires_delta: timedelta = None) -> str:
    """Generate JWT token."""
    if expires_delta is None:
        expires_delta = timedelta(hours=1)  # Default expiration time of 1 hour    
    # Define JWT payload
    payload = {
        "email": email,
        "exp": datetime.utcnow() + expires_delta,  # Add expiration time to current time
    }
    # Encode and return the JWT token
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

# Helper function to decode and verify the JWT token
def decode_jwt_token(token: str) -> dict:
    """Decode and verify JWT token."""
    try:
        # Decode the token with the provided secret key and algorithm
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")


# User Signup Endpoint
@router.post("/signup", response_model=UserResponse)
async def signup(user: UserCreate):
    """
    Signup endpoint for user to create an account.
    """
    # Validate passwords match
    if user.password != user.confirm_password:
        raise HTTPException(status_code=400, detail="Passwords do not match")
    # Check if the user already exists
    existing_user = await sync_to_async(lambda: Userm.objects.filter(email=user.email).first())()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    # Create new user
    hashed_password = bcrypt.hash(user.password)
    new_user = Userm(email=user.email, password=hashed_password)
    await sync_to_async(new_user.save)()
    return UserResponse(email=new_user.email, role='user', is_active=True)


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
# User Login Endpoint
@router.post("/login", response_model=LoginResponse)
async def login(request:Request,credentials:LoginRequest):
    """Validate user credentials and perform login."""    
    try:
        # Fetch the user from the database using email
        user = await sync_to_async(Userm.objects.get)(email=credentials.email)
    except Userm.DoesNotExist:
        raise HTTPException(status_code=401, detail="Invalid credentials")    
    # Check if the password hash is in a valid format
    try:
        # If the password hash is not valid, this will raise an UnknownHashError
        if not pwd_context.verify(credentials.password, user.password):
            raise HTTPException(status_code=401, detail="Invalid credentials")
    except UnknownHashError:
        # If the hash is unrecognized, rehash and save it
        hashed_password = pwd_context.hash(password)
        user.password = hashed_password
        await sync_to_async(user.save)()  # Save the updated user with the new hashed password
        if not pwd_context.verify(credentials.password, user.password):
            raise HTTPException(status_code=401, detail="Invalid credentials")
    # Generate JWT token for the authenticated user
    token = create_jwt_token(email=user.email)  
    request.session["access_token"] = token             # Store token in session (cookie) 
    return LoginResponse(message="Login successful", token=token)

# User Logout Endpoint
@router.post("/logout")
async def logout(request: Request, response: Response):
    """Logout user by clearing the session."""
    if "access_token" in request.session:
        del request.session["access_token"]  # Remove the access token from the session
        response.delete_cookie("session")  # Optional: delete the cookie explicitly
        return {"message": "Logout successful"}
    else:
        raise HTTPException(status_code=400, detail="No active session")

@router.post("/refresh-session")
async def refresh_session(request: Request):
    """Refresh the session if the user interacts with the screen."""
    token = request.session.get("access_token")
    if not token:
        raise HTTPException(status_code=401, detail="No active session")    
    # Decode and validate the token
    try:
        payload = decode_jwt_token(token)               
        # Check if the token is expired
        email = payload["email"]
        if payload["exp"] < datetime.utcnow().timestamp():
            raise HTTPException(status_code=401, detail="Token has expired")        
        return {"message": "Session is active", "email": email}
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")  
  
  
import os
from random import randint
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build


# In-memory store for OTPs (use a DB in production)
otp_store = {}
# Email settings (OAuth2 credentials will handle this for you)
FROM_EMAIL = "alishersoftdev@gmail.com"  # Use your authenticated Gmail account here
# OAuth2 scopes and credentials
SCOPES = ['https://www.googleapis.com/auth/gmail.send']
creds = None

# Token management (using stored credentials or new authentication)
if os.path.exists('token.json'):
    creds = Credentials.from_authorized_user_file('token.json', SCOPES)
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            'E:\\Programming\\alldjangoprojects\\ecommerce_project\\credentials.json', SCOPES
        )
        creds = flow.run_local_server(port=0)

    # Save the token for reuse
    with open('token.json', 'w') as token:
        token.write(creds.to_json())

# Build Gmail API service
service = build('gmail', 'v1', credentials=creds)

# Generate a random OTP
def generate_otp():
    return str(randint(1000, 9999))  # 4-digit OTP

# Send OTP via email
def send_otp_email(email, otp):
    try:
        message = MIMEMultipart()
        message['to'] = email
        message['from'] = FROM_EMAIL
        message['subject'] = 'Your OTP Code'
        body = f"Your OTP code is {otp}. It will expire in 5 minutes."
        msg = MIMEText(body, 'plain')
        message.attach(msg)

        raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

        # Send the email
        message = service.users().messages().send(userId="me", body={'raw': raw_message}).execute()
        print(f"OTP sent to {email} with message ID: {message['id']}")
        return message
    except Exception as e:
        print(f"An error occurred: {e}")
        raise HTTPException(status_code=500, detail="Failed to send OTP via email")


# API to request OTP (for login, signup, etc.)
@router.post("/generate-otp")
async def generate_otp_for_user(request: OTPRequest):
    email = request.email
    # Generate OTP
    otp = generate_otp()
    # Store OTP and its expiration time in memory (or use a DB in production)
    otp_store[email] = {
        "otp": otp,
        "expires_at": datetime.utcnow() + timedelta(minutes=5),  # OTP expires in 5 minutes
    }
    # Send OTP (via email or SMS)
    send_otp_email(email, otp)  # Use send_otp_sms if you want SMS instead
    return {"message": "OTP sent successfully"}

# API to verify OTP
@router.post("/verify-otp")
async def verify_otp(request: OTPVerification):
    email = request.email
    otp = request.otp
    # Check if OTP exists in memory store
    otp_data = otp_store.get(email)
    if not otp_data:
        raise HTTPException(status_code=400, detail="No OTP request found for this email")
    if datetime.utcnow() > otp_data["expires_at"]:
        # OTP expired
        del otp_store[email]  # Remove expired OTP from store
        raise HTTPException(status_code=400, detail="OTP has expired")
    if otp_data["otp"] != otp:
        raise HTTPException(status_code=400, detail="Invalid OTP")
    # OTP is valid, so clear it from the store
    del otp_store[email]
    return {"message": "OTP verified successfully"}

    
# API Key Generation Endpoint
@router.post("/agenerate-api-key", response_model=KeyGenerationResponse)
async def generate_api_key():
    """Generate a single API key for user-related endpoints."""
    raw_key = "USER_" + str(uuid.uuid4())
    wrapped_key = base64.urlsafe_b64encode(raw_key.encode()).decode()

    api_key = APIKey(key=wrapped_key, expires_at=datetime.utcnow() + timedelta(days=30))
    await sync_to_async(api_key.save)()

    return KeyGenerationResponse(api_key=wrapped_key, expires_at=api_key.expires_at)


