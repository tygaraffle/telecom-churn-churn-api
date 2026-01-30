# Dockerfile
# Creates a "container" — an isolated little bubble inside the server that thinks it’s its own mini computer.
# Container= The mini computer created everytime to run our app.

# 1. START WITH A BASE IMAGE
# Use official Python slim image (smaller size, just essentials)
# You’re telling Docker, "Start with a tiny, clean version of Linux that already has Python 3.11 installed." No extra junk.
FROM python:3.11-slim

# 2. SET WORKING DIRECTORY INSIDE CONTAINER
# Inside this "mini computer," create a folder called app and move into it.
WORKDIR /app

# 3. INSTALL SYSTEM DEPENDENCIES (if any)
# Some Python packages need system libraries to compile
# Example: gcc for compiling, curl for health checks
RUN apt-get update && apt-get install -y \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/*  
    
# 4. COPY REQUIREMENTS FILE FIRST
# You’re installing your ML libraries that u stored in "C:3)Telecome-churn-prediction proj\api\requirements.txt",
# (like fastapi or joblib) inside the image so they are baked in forever.
# Docker will cache this layer, so if requirements don't change,
# it won't reinstall dependencies every build
COPY api/requirements.txt .

# 5. INSTALL PYTHON DEPENDENCIES
# Install all Python packages listed in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# 6. COPY APPLICATION CODE
# Copy all our source code into the container
# Copy in this order to optimize caching:
# 1. API code
# 2. Models
# 3. Source modules
#For example in the line below You’re moving your churn predictor code into that specific internal folder.
COPY api/ ./api/        
COPY models/ ./models/
COPY src/ ./src/

# 7. CREATE A NON-ROOT USER (SECURITY BEST PRACTICE)
# Running as root is dangerous. Create a regular user instead.
# WHY: By default, Docker containers run as root (the Super Admin). This means anyone can delete your ML models, 
# Steal your database credentials, or change your churn logic.
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

#Just telling Docker where your app.py or API is located, BUT the door to it is still locked.
#Useful because it helps Docker in many ways.
EXPOSE 8000

# 9. HEALTH CHECK (OPTIONAL BUT RECOMMENDED)
# Docker can monitor if our API is healthy
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# HEALTHCHECK (The Heartbeat)
#What it is: A recurring "medical checkup" that Docker performs on your app while it’s running.
#What it’s doing in your project: Every 30 seconds (--interval=30s), Docker runs a tiny curl command (basically an invisible browser click) to your app’s /health page.
#If the app answers "I'm okay": Docker shows a green "healthy" status.
#If the app crashes or freezes: The check fails. After 3 tries (--retries=3), Docker marks the container as "unhealthy."
#Why do you need this for a Churn Predictor?
#Imagine your ML model uses too much RAM and the app freezes. To the outside world, the container looks like it's still "Running," but it's actually "Brain Dead."
#The HEALTHCHECK catches this. On platforms like AWS or Render, if the health check fails, the platform will automatically kill the dead container and start a fresh one for you. It’s "self-healing" code!


# 10. COMMAND TO RUN WHEN CONTAINER STARTS
# This runs when someone does: docker run your-image
# Starts Uvicorn server with our FastAPI app
# IMP!!: We need to have this CMD line of code at the end of every docker code file because without it, 
# Docker builds the "box," looks around, realizes it has no job to do, and immediately shuts down.
CMD ["uvicorn", "api.app:app", "--host", "0.0.0.0", "--port", "8000"]