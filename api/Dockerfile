# Stage 1: Base image for building the application
FROM python:3.12 AS builder

# Set the working directory
WORKDIR /build

# Copy the requirements file
COPY requirements.txt .

# Create a virtual environment and install required dependencies
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
RUN pip install --no-cache-dir -r requirements.txt

# ==========================================
# Stage 2: Production Runtime
# ==========================================
FROM python:3.12-slim AS runtime

# Install tini for proper PID 1 signal handling
# hadolint ignore=DL3008
RUN apt-get update && apt-get install -y --no-install-recommends tini \
    && rm -rf /var/lib/apt/lists/*

# Copy the pre-built virtual environment from the builder stage
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Set the working directory
WORKDIR /app

# Copy the application code
COPY main.py .

# Create a non-root user
RUN groupadd -r fastapiuser && useradd -r -g fastapiuser fastapiuser

# Change ownership of the app directory and cache
RUN chown -R fastapiuser:fastapiuser /app \
    && mkdir -p /home/fastapiuser && chown fastapiuser:fastapiuser /home/fastapiuser

# Switch to the non-root user
USER fastapiuser

# HEALTHCHECK: Verify the API is responsive
HEALTHCHECK --interval=10s --timeout=5s --start-period=30s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')" || exit 1

# Expose the application port
EXPOSE 8000

# Use tini to manage signals properly
ENTRYPOINT ["/usr/bin/tini", "--"]

# Start Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]