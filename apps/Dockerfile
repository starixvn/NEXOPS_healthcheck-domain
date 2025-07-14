FROM hub.nexdev.net/base/python:3.10-alpine

WORKDIR /app

# Copy script + requirement
COPY app.py requirements.txt ./

# COPY Domain list
COPY ../domains domains/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

## Entry point
CMD ["python3", "app.py"]