# eCommerce Project
This project integrates **Django** for handling data analysis, third-party API integration, and user management, and
**FastAPI** for user authentication and JWT token management. The project is structured into several sub-applications that work together to provide the following functionalities:
## Project Structure
| Directory / File              | Description         |
|-------------------------------|---------------------|
| `ecommerce_project/`           | Root project folder |
| `├── ecommerce_project/`       | Main app folder     |
| `│   ├── __init__.py`          | Initialization file |
| `│   ├── settings.py`          | Settings file       |
| `│   ├── urls.py`              | URLs configuration  |
| `│   ├── wsgi.py`              | WSGI entry point    |
| `│   ├── asgi.py`              | ASGI entry point    |
| `├── fastapidjango/`           | FastAPI app folder  |
| `│   ├── __init__.py`          | Initialization file |
| `│   ├── user_api.py`          | User API module     |
| `│   ├── models.py`            | Data models         |
| `│   ├── schemas.py`           | Pydantic schemas    |
| `│   ├── utils.py`             | Utility functions   |
| `├── datanalysisapp/`          | Django app for data analysis |
| `│   ├── __init__.py`          | Initialization file |
| `│   ├── models.py`            | Data models         |
| `│   ├── views.py`             | Views for analysis  |
| `│   ├── forms.py`             | Forms for upload    |
| `│   ├── urls.py`              | URLs for analysis   |
| `│   └── templates/`           | HTML templates      |
| `├── thirdpartyapiapp/`        | Third-party APIs    |
| `│   ├── __init__.py`          | Initialization file |
| `│   ├── views.py`             | Views for APIs      |
| `│   ├── models.py`            | API models          |
| `│   ├── urls.py`              | URLs for APIs       |
| `│   └── templates/`           | HTML templates      |
| `├── users/`                   | User management     |
| `│   ├── __init__.py`          | Initialization file |
| `│   ├── models.py`            | User models         |
| `│   ├── views.py`             | Views for users     |
| `│   ├── forms.py`             | Forms for users     |
| `│   ├── urls.py`              | URLs for user ops   |
| `│   └── templates/`           | User templates      |
| `├── manage.py`                | Django management   |
| `├── requirements.txt`         | Dependencies        |


## Project Flow
### FastAPI
- **User Authentication**: FastAPI handles user authentication, including login, signup, and JWT token generation.
- **Endpoints**: FastAPI provides endpoints for user-related operations such as login, signup, and token refresh.
### Django
- **Data Analysis**: Django handles data analysis functionalities, including uploading data and viewing analysis results.
- **Third-Party API Integration**: Django integrates with third-party APIs to fetch weather and stock data.
- **User Management**: Django manages user-related operations such as login, signup, and OTP verification.

## Functionalities

- **User Authentication**: Users can sign up, log in, and refresh their session using JWT tokens through FastAPI.
- **Data Analysis**: Users can upload data files (e.g., CSV), and the system performs data analysis and displays the results through Django.
- **Third-Party API Integration**: The system fetches weather and stock data from third-party APIs (e.g., Weather API, Stock API) and displays it to the user.

## Subapps
 ### fastapidjango
- **Purpose**: Handles user authentication and JWT token management using FastAPI.
- **Files**:
  - **user_api**.py: Defines endpoints for user-related operations.
  - **models.py**: Defines database models for user data.
  - **schemas.py**: Defines Pydantic schemas for request and response validation.
  - **utils.py**: Contains utility functions for JWT token creation and verification.

### datanalysisapp

- **Purpose**: Handles data analysis functionalities using Django.
- **Files**:
  - **models.py**: Defines database models for uploaded data and analysis results.
  - **views.py**: Defines views for uploading data and viewing analysis results.
  - **forms.py**: Defines forms for data upload.
  - **urls.py**: Defines URL patterns for the app.
  - **templates/**: Contains HTML templates for data upload and analysis results.

### thirdpartyapiapp

- **Purpose**: Integrates with third-party APIs to fetch weather and stock data using Django.
- **Files**:
  - **models.py**: Defines database models for weather and stock data.
  - **views.py**: Defines views for fetching and displaying weather and stock data.
  - **urls.py**: Defines URL patterns for the app.
  - **templates**/: Contains HTML templates for weather and stock data.

### users

- **Purpose**: Manages user-related operations such as login, signup, and OTP verification using Django.
- **Files**:
  - **models.py**: Defines database models for user data.
  - **views.py**: Defines views for user-related operations.
  - **forms.py**: Defines forms for user login and signup.
  - **urls.py**: Defines URL patterns for the app.
  - **templates**: Contains HTML templates for user login and signup.

## Packages Used

- **Django**: Web framework for handling data analysis, third-party API integration, and user management.
- **FastAPI**: Web framework for handling user authentication and JWT token management.
- **Pandas**: Data analysis library used for processing uploaded data.
- **Requests**: HTTP library used for making API calls to third-party services.
- **JWT**: Library for creating and verifying JSON Web Tokens.
- **Passlib**: Library for hashing passwords.
- **ASGI**: Asynchronous Server Gateway Interface for handling asynchronous requests.
- **WSGI**: Web Server Gateway Interface for handling synchronous requests.

## How to Run the Project

### 1. Clone the repository
git clone https://github.com/codebyalisher/ecommerce_project.git <br>
cd ecommerce_project
--
### 2. Install dependencies
#### Use pip to install the required dependencies from the requirements.txt file.
pip install -r requirements.txt
--
### 3. Run Django server
#### To start the Django development server (default port 8000):
python manage.py runserver
--
### 4. Run FastAPI server 
To start the FastAPI server (default port 8000): <br>
Run these commands <br>
cd fastapidjango & fastapi dev main.py
--
### 5. Access the application
Django: Access the Django application at http://127.0.0.1:8001 <br>
FastAPI: Access the FastAPI application at http://127.0.0.1:8000/docs (for API documentation)
--
## License 
This project is licensed under the MIT License. See the LICENSE file for details.
This **`README.md`** file follows Markdown syntax and contains all the details about the structure, functionality, setup, and how to run your project. You can copy and paste this into your `README.md` file in your project.
