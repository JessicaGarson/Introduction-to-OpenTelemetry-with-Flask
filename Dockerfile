# Use an Alpine Linux base image
FROM alpine:latest

# Install utilities for downloading and user management
RUN apk add --no-cache shadow wget tar

# Create a user named `otel` with UID 1001
RUN useradd -u 1001 -m -s /bin/bash otel

# Switch to the otel user
USER otel

# Download and extract the OpenTelemetry Collector binary manually
RUN wget -O /otelcol.tar.gz https://github.com/open-telemetry/opentelemetry-collector-releases/releases/download/v0.86.0/otelcol_0.86.0_Linux_x86_64.tar.gz && \
    tar -zxvf /otelcol.tar.gz -C /usr/local/bin

# Copy the OpenTelemetry Collector configuration
COPY otel-collector-config.yaml /etc/otel-collector-config.yaml

# Start the OpenTelemetry Collector with the provided configuration
CMD ["otelcol", "--config=/etc/otel-collector-config.yaml"]