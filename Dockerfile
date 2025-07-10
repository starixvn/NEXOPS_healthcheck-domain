FROM python:3.11-slim

WORKDIR /app

# Copy script + requirement
COPY app.py requirements.txt ./

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Entry point
CMD ["python", "app.py"]