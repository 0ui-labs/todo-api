# Monitoring & Observability Guide

This guide covers the monitoring and observability features implemented in the Todo API, including metrics collection, structured logging, and distributed tracing.

## Table of Contents

- [Overview](#overview)
- [Metrics](#metrics)
- [Logging](#logging)
- [Distributed Tracing](#distributed-tracing)
- [Configuration](#configuration)
- [Integration with Monitoring Tools](#integration-with-monitoring-tools)
- [Dashboards and Alerts](#dashboards-and-alerts)

## Overview

The Todo API implements comprehensive monitoring and observability using:

- **Prometheus** for metrics collection
- **OpenTelemetry** for distributed tracing
- **Structured JSON logging** with correlation IDs
- **Custom business metrics** for application insights

## Metrics

### Available Metrics

#### HTTP Metrics
- `http_requests_total` - Total HTTP requests by method, endpoint, and status
- `http_request_duration_seconds` - Request duration histogram
- `http_requests_in_progress` - Current number of requests being processed
- `rate_limit_exceeded_total` - Rate limit violations by endpoint
- `errors_total` - Errors by type and endpoint

#### Database Metrics
- `db_query_total` - Database queries by operation and table
- `db_query_duration_seconds` - Query execution time
- `db_connections_active` - Active database connections
- `db_connections_idle` - Idle database connections

#### Cache Metrics
- `cache_hits_total` - Cache hits by namespace
- `cache_misses_total` - Cache misses by namespace
- `cache_sets_total` - Cache set operations
- `cache_deletes_total` - Cache delete operations

#### Business Metrics
- `todos_created_total` - Total todos created
- `todos_completed_total` - Total todos marked as completed
- `todos_deleted_total` - Total todos deleted
- `users_registered_total` - Total user registrations
- `users_login_total` - User logins by status (success/failure)

### Accessing Metrics

Metrics are exposed at the `/metrics` endpoint in Prometheus format:

```bash
curl http://localhost:8000/metrics
```

Example output:
```
# HELP http_requests_total Total HTTP requests
# TYPE http_requests_total counter
http_requests_total{method="GET",endpoint="/api/v1/todos",status="200"} 42.0
http_requests_total{method="POST",endpoint="/api/v1/todos",status="201"} 15.0

# HELP http_request_duration_seconds HTTP request duration in seconds
# TYPE http_request_duration_seconds histogram
http_request_duration_seconds_bucket{method="GET",endpoint="/api/v1/todos",le="0.1"} 40.0
http_request_duration_seconds_bucket{method="GET",endpoint="/api/v1/todos",le="0.5"} 42.0
```

## Logging

### Structured Logging

The API uses structured JSON logging with the following fields:

```json
{
  "timestamp": "2025-01-24T10:30:45.123Z",
  "severity": "INFO",
  "logger": "app.api.todos",
  "message": "Request completed",
  "request_id": "550e8400-e29b-41d4-a716-446655440000",
  "user_id": "123",
  "trace_id": "5c3a5b7d9e2f4a6b8c1d2e3f4a5b6c7d",
  "span_id": "8e9f0a1b2c3d4e5f",
  "method": "GET",
  "path": "/api/v1/todos",
  "status_code": 200,
  "process_time": 0.045,
  "source": {
    "file": "/app/api/todos.py",
    "line": 78,
    "function": "get_todos"
  }
}
```

### Correlation IDs

Every request is assigned a unique Request ID for tracing through the system:
- Available in logs as `request_id`
- Returned in response header `X-Request-ID`
- Automatically propagated to all log entries during request processing

### Log Levels

Configure log level via environment variable:
```bash
LOG_LEVEL=DEBUG  # DEBUG, INFO, WARNING, ERROR, CRITICAL
```

### Viewing Logs

In development (human-readable):
```bash
JSON_LOGS=false uvicorn app.main:app --reload
```

In production (JSON format):
```bash
JSON_LOGS=true uvicorn app.main:app
```

## Distributed Tracing

### OpenTelemetry Integration

The API is instrumented with OpenTelemetry for distributed tracing:

1. **Automatic Instrumentation**
   - FastAPI endpoints
   - SQLAlchemy queries
   - Redis operations
   - HTTP client requests

2. **Manual Instrumentation**
   ```python
   from app.monitoring.tracing import trace_async, add_span_attributes
   
   @trace_async("process_todo")
   async def process_todo(todo_id: str):
       add_span_attributes(todo_id=todo_id, action="process")
       # Your code here
   ```

### Trace Context

Trace and Span IDs are automatically:
- Generated for each request
- Added to structured logs
- Propagated to downstream services
- Available in response headers for debugging

### Exporting Traces

Configure OTLP endpoint for trace export:
```bash
OTLP_ENDPOINT=http://localhost:4317
```

Supported backends:
- Jaeger
- Grafana Tempo
- AWS X-Ray
- Google Cloud Trace

## Configuration

### Environment Variables

```bash
# Logging
LOG_LEVEL=INFO                    # Logging level
JSON_LOGS=true                    # Enable JSON structured logging

# OpenTelemetry
OTLP_ENDPOINT=http://localhost:4317  # OTLP collector endpoint
OTEL_SERVICE_NAME=todo-api          # Service name for traces
OTEL_SERVICE_VERSION=1.0.0          # Service version

# Metrics
METRICS_ENABLED=true                 # Enable metrics collection
```

### Programmatic Configuration

```python
# In app/main.py
from app.monitoring.telemetry import setup_telemetry
from app.monitoring.logging_config import setup_logging

# Setup structured logging
setup_logging(
    level="INFO",
    json_logs=True,
    service_name="todo-api"
)

# Setup OpenTelemetry
setup_telemetry(
    service_name="todo-api",
    service_version="1.0.0",
    otlp_endpoint="http://localhost:4317"
)
```

## Integration with Monitoring Tools

### Prometheus Setup

1. Add to `prometheus.yml`:
```yaml
scrape_configs:
  - job_name: 'todo-api'
    static_configs:
      - targets: ['localhost:8000']
    metrics_path: '/metrics'
    scrape_interval: 15s
```

2. Start Prometheus:
```bash
prometheus --config.file=prometheus.yml
```

### Grafana Setup

1. Add Prometheus data source
2. Import dashboard (see `monitoring/dashboards/todo-api-dashboard.json`)
3. Configure alerts based on metrics

### Jaeger Setup

1. Start Jaeger:
```bash
docker run -d --name jaeger \
  -p 16686:16686 \
  -p 4317:4317 \
  jaegertracing/all-in-one:latest
```

2. Configure OTLP endpoint:
```bash
OTLP_ENDPOINT=http://localhost:4317
```

3. View traces at http://localhost:16686

## Dashboards and Alerts

### Key Metrics to Monitor

1. **Service Health**
   - Request rate: `rate(http_requests_total[5m])`
   - Error rate: `rate(http_requests_total{status=~"5.."}[5m])`
   - P95 latency: `histogram_quantile(0.95, http_request_duration_seconds)`

2. **Database Performance**
   - Query rate: `rate(db_query_total[5m])`
   - Slow queries: `db_query_duration_seconds > 1`
   - Connection pool usage: `db_connections_active / (db_connections_active + db_connections_idle)`

3. **Cache Efficiency**
   - Hit rate: `rate(cache_hits_total[5m]) / (rate(cache_hits_total[5m]) + rate(cache_misses_total[5m]))`
   - Cache operations: `rate(cache_sets_total[5m]) + rate(cache_deletes_total[5m])`

4. **Business Metrics**
   - Todo creation rate: `rate(todos_created_total[1h])`
   - User activity: `rate(users_login_total{status="success"}[1h])`
   - Failed logins: `rate(users_login_total{status="failure"}[5m])`

### Example Alerts

```yaml
groups:
  - name: todo-api
    rules:
      - alert: HighErrorRate
        expr: rate(http_requests_total{status=~"5.."}[5m]) > 0.05
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: High error rate detected
          
      - alert: SlowQueries
        expr: db_query_duration_seconds > 1
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: Database queries taking >1s
          
      - alert: LowCacheHitRate
        expr: |
          rate(cache_hits_total[5m]) / 
          (rate(cache_hits_total[5m]) + rate(cache_misses_total[5m])) < 0.8
        for: 10m
        labels:
          severity: warning
        annotations:
          summary: Cache hit rate below 80%
```

## Best Practices

1. **Use Structured Logging**
   - Always use logger with `extra` fields
   - Include relevant context (user_id, resource_id)
   - Keep messages concise and consistent

2. **Add Custom Spans**
   - Instrument critical business logic
   - Add meaningful attributes to spans
   - Use consistent naming conventions

3. **Monitor Business Metrics**
   - Track key business KPIs
   - Use metrics to understand user behavior
   - Set up alerts for anomalies

4. **Performance Considerations**
   - Metrics collection has minimal overhead
   - Use sampling for high-volume traces
   - Aggregate logs before shipping to reduce volume

## Troubleshooting

### Metrics Not Appearing

1. Check if metrics endpoint is accessible:
   ```bash
   curl http://localhost:8000/metrics
   ```

2. Verify Prometheus scraping:
   - Check Prometheus targets page
   - Look for scrape errors

### Missing Traces

1. Verify OTLP endpoint configuration
2. Check OpenTelemetry SDK initialization
3. Look for errors in application logs

### Log Correlation Issues

1. Ensure middleware order is correct
2. Verify context propagation in async code
3. Check for cleared context variables

## Development Tools

### Local Monitoring Stack

Use the provided Docker Compose for local development:

```bash
cd monitoring
docker-compose up -d
```

This starts:
- Prometheus (http://localhost:9090)
- Grafana (http://localhost:3000)
- Jaeger (http://localhost:16686)

### Testing Metrics

Run the monitoring tests:
```bash
pytest tests/unit/test_monitoring_*.py -v
pytest tests/integration/test_monitoring_integration.py -v
```

## Performance Impact

The monitoring implementation has minimal performance impact:
- Metrics collection: <1ms per request
- Structured logging: <0.5ms per log entry
- Tracing: ~2-5% overhead (configurable via sampling)

All monitoring features can be disabled via configuration if needed.