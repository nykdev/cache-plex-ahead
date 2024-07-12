FROM python:3.9-alpine

# Install dependencies
RUN apk add --no-cache gcc musl-dev \
    && pip3 install --no-cache-dir plexapi flask flask_apispec waitress

# Copy script to the container
COPY ./cache_webhook.py /opt/scripts/cache_webhook.py

# Set environment variable
ENV FLASK_ENV=development

# Set the working directory
WORKDIR /opt/scripts

# Expose the port the app runs on
EXPOSE 6969

# Run the application
CMD ["python3", "cache_webhook.py"]
