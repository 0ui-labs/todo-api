# Todo API Monitoring Stack

This directory contains the monitoring stack configuration for the Todo API.

## Quick Start

1. Start the monitoring stack:
```bash
docker-compose up -d
```

2. Access the services:
- **Prometheus**: http://localhost:9090
- **Grafana**: http://localhost:3000 (admin/admin)
- **Jaeger**: http://localhost:16686
- **Loki**: http://localhost:3100

3. Configure the Todo API to export metrics:
```bash
# In your .env file
OTLP_ENDPOINT=http://localhost:4317
JSON_LOGS=true
LOG_LEVEL=INFO
```

## Services

### Prometheus
- Collects metrics from the Todo API `/metrics` endpoint
- Configured to scrape every 15 seconds
- Alerts are defined in `alerts.yml`

### Grafana
- Pre-configured with Prometheus, Jaeger, and Loki datasources
- Includes a sample Todo API dashboard
- Default credentials: admin/admin

### Jaeger
- Collects distributed traces via OTLP
- Supports both gRPC (4317) and HTTP (4318) protocols
- UI available at port 16686

### Loki (Optional)
- Aggregates logs from the Todo API
- Works with Promtail for log shipping
- Integrated with Grafana for log exploration

## Configuration Files

- `docker-compose.yml` - Main orchestration file
- `prometheus.yml` - Prometheus scrape configuration
- `alerts.yml` - Alert rules for Prometheus
- `datasources/` - Grafana datasource configurations
- `dashboards/` - Grafana dashboard definitions
- `loki-config.yaml` - Loki configuration

## Customization

### Adding Custom Alerts

Edit `alerts.yml` and add your alert rules:
```yaml
- alert: MyCustomAlert
  expr: some_metric > threshold
  for: 5m
  labels:
    severity: warning
  annotations:
    summary: "Alert summary"
```

### Creating Custom Dashboards

1. Create dashboards in Grafana UI
2. Export as JSON
3. Save to `dashboards/` directory
4. Restart Grafana container

### Modifying Scrape Targets

Edit `prometheus.yml` to add new targets:
```yaml
- job_name: 'my-service'
  static_configs:
    - targets: ['localhost:8001']
```

## Troubleshooting

### Prometheus Can't Scrape Metrics
- Check if Todo API is running
- Verify the target address in `prometheus.yml`
- Use `host.docker.internal` instead of `localhost` on Mac/Windows

### Grafana Can't Connect to Datasources
- Ensure all containers are on the same network
- Check datasource URLs in `datasources/prometheus.yml`

### No Traces in Jaeger
- Verify OTLP_ENDPOINT is configured in Todo API
- Check Jaeger logs for connection errors
- Ensure port 4317 is accessible

## Production Considerations

For production deployment:
1. Use persistent volumes for data storage
2. Configure proper authentication for Grafana
3. Set up alerting channels (email, Slack, etc.)
4. Use external storage backends for scalability
5. Implement proper backup strategies