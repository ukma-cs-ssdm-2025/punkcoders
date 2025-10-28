# Base Image
FROM python:3.12-slim AS base
# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
# Set working directory
WORKDIR /app
# Copy project files
COPY ./delivery-service/ /app/
COPY requirements/ /app/requirements

FROM base AS development
# Install dependencies
RUN pip install --no-cache-dir -r requirements/dev.txt
# run the thing
CMD ["sh", "/app/startup.sh"]

FROM base AS production
# Install dependencies
RUN pip install --no-cache-dir -r requirements/prod.txt
# Ensure the startup script is executable
RUN chmod +x /app/startup.sh
# run the thing
CMD ["sh", "/app/startup.sh"]