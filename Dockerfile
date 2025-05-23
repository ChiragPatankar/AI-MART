# Build React frontend
FROM node:18 as frontend-build
WORKDIR /app/frontend
COPY frontend ./ 
RUN npm install && npm run build

# Build Python backend with Uvicorn
FROM python:3.10
WORKDIR /app

# Copy backend source
COPY src ./src
COPY main.py requirements.txt .env ./

# Copy built frontend
COPY --from=frontend-build /app/frontend/build ./frontend_build

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port (make sure your app runs on this port)
EXPOSE 7860

# Start FastAPI and serve frontend
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7860"]
