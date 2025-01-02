#!/bin/bash
# Run migrations
python manage.py migrate

# Start the Django development server
python manage.py runserver 0.0.0.0:8001 &

# Wait for the server to start, then open it in the browser (use the host IP)
sleep 5

# Open the browser (Linux/MacOS/Windows)
xdg-open http://localhost:8001/ || open http://localhost:8001/ || start http://localhost:8001/