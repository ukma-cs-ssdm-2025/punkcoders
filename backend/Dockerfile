# Base Image
FROM python:3.12-slim AS development

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY ./delivery-service/ /app/

CMD ["sh", "/app/startup.sh"]

# ----- Stage 2: Production Stage -----
# This stage builds on top of the dev stage
FROM development AS production
# Add gunicorn
RUN pip install gunicorn
# Ensure the startup script is executable
RUN chmod +x /app/startup.sh
# The command for production (assumes .startup.sh runs gunicorn)
CMD ["sh", ".startup.sh"]