# Base Image
FROM python:3.12-slim AS base
# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
# Set working directory
WORKDIR /app
# Copy project files
COPY ./delivery-service/ /app/

FROM base AS development
# Install dependencies
COPY requirements/dev.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
# run the thing
CMD ["sh", "/app/startup.sh"]

FROM base AS production
# Install dependencies
COPY requirements/prod.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
# Ensure the startup script is executable
RUN chmod +x /app/startup.sh
# run the thing
CMD ["sh", "/app/startup.sh"]