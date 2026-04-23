# Base image
FROM nginx:alpine

# Remove default nginx configuration
RUN rm /etc/nginx/conf.d/default.conf

# Copy custom nginx configuration
COPY nginx.conf /etc/nginx/nginx.conf

# Copy the static frontend files to the nginx html directory
COPY views/index.html /usr/share/nginx/html/

# Ensure nginx owns the necessary nginx runtime directories to avoid permission issues when nginx tries to write logs or manage its PID file.
RUN chown -R nginx:nginx /var/cache/nginx \
    && chown -R nginx:nginx /var/run \
    && chown -R nginx:nginx /usr/share/nginx/html

# Switch to the 'nginx' user for better security
USER nginx

# Expose port 8080
EXPOSE 8080

# Healthcheck to ensure nginx is running and serving content
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD wget -qO- http://localhost:8080/ || exit 1
# HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
#     CMD curl -f http://localhost:8080/ || exit 1

# Start nginx in the foreground
CMD ["nginx", "-g", "daemon off;"]