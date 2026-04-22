# Base image for stage 1: Build the application
FROM python:3.12 AS builder

# Set the working directory
WORKDIR /build

# Copy the requirements file and install dependencies
COPY requirements.txt .

# Create a virtual environment and install dependencies
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
RUN pip install --no-cache-dir -r requirements.txt 

# Stage 2: Create the final image for production runtime
FROM python:3.12-slim AS runtime

# Install tini for proper PID 1 signal handling
RUN apt-get update && apt-get install -y --no-install-recommends tini curl \
    && rm -rf /var/lib/apt/lists/*

# Copy the pre-built virtual environment from the builder stage
COPY --from=builder /opt/venv /opt/venv

# Set the working directory
WORKDIR /app

# Copy the application code
COPY worker.py .

# Create a non-root user and switch to it
RUN groupadd -r workeruser && useradd -r -g workeruser workeruser

# Change ownership of the application directory to the non-root user
RUN chown -R workeruser:workeruser /app

# Switch to the non-root user
USER workeruser

# HEALTHCHECK: Verify the worker can actually reach Redis using the runtime env vars
# This ensures both the process is alive AND its network dependencies are met
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD python -c "import redis, os; r=redis.Redis(host=os.getenv('REDIS_HOST', 'localhost'), port=int(os.getenv('REDIS_PORT', 6379))); r.ping()" || exit 1

# Use tini as the entrypoint to handle signals properly
ENTRYPOINT ["/usr/bin/tini", "--"]

# Command to run the worker
CMD ["/opt/venv/bin/python", "worker.py"]