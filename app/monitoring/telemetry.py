"""OpenTelemetry configuration and setup."""
import os

from opentelemetry import metrics, trace
from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor

# Optional instrumentations - may not be installed
try:
    from opentelemetry.instrumentation.redis import RedisInstrumentor
except ImportError:
    RedisInstrumentor = None

try:
    from opentelemetry.instrumentation.httpx import HTTPXClientInstrumentor
except ImportError:
    HTTPXClientInstrumentor = None
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.sdk.resources import SERVICE_NAME, SERVICE_VERSION, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor


def setup_telemetry(
    service_name: str = "todo-api",
    service_version: str = "1.0.0",
    otlp_endpoint: str | None = None
) -> tuple[TracerProvider, MeterProvider]:
    """Setup OpenTelemetry tracing and metrics.

    Args:
        service_name: Name of the service
        service_version: Version of the service
        otlp_endpoint: OTLP endpoint for exporting telemetry data

    Returns:
        Tuple of (TracerProvider, MeterProvider)
    """
    # Create resource
    resource = Resource.create({
        SERVICE_NAME: service_name,
        SERVICE_VERSION: service_version,
        "service.environment": os.getenv("ENVIRONMENT", "development"),
        "service.instance.id": os.getenv("HOSTNAME", "localhost"),
    })

    # Setup tracing
    tracer_provider = TracerProvider(resource=resource)

    if otlp_endpoint:
        # Export traces to OTLP endpoint (e.g., Jaeger, Grafana Tempo)
        otlp_exporter = OTLPSpanExporter(
            endpoint=otlp_endpoint,
            insecure=True  # Use secure=False for local development
        )
        tracer_provider.add_span_processor(
            BatchSpanProcessor(otlp_exporter)
        )

    trace.set_tracer_provider(tracer_provider)

    # Setup metrics
    if otlp_endpoint:
        metric_reader = PeriodicExportingMetricReader(
            exporter=OTLPMetricExporter(
                endpoint=otlp_endpoint,
                insecure=True
            ),
            export_interval_millis=30000  # Export every 30 seconds
        )
        meter_provider = MeterProvider(
            resource=resource,
            metric_readers=[metric_reader]
        )
    else:
        meter_provider = MeterProvider(resource=resource)

    metrics.set_meter_provider(meter_provider)

    return tracer_provider, meter_provider


def instrument_app(app, engine=None):
    """Instrument the FastAPI application and its dependencies.

    Args:
        app: FastAPI application instance
        engine: SQLAlchemy engine instance
    """
    # Instrument FastAPI
    FastAPIInstrumentor.instrument_app(app)

    # Instrument SQLAlchemy if engine is provided
    if engine:
        SQLAlchemyInstrumentor().instrument(
            engine=engine,
            service="todo-api-db"
        )

    # Instrument Redis if available
    if RedisInstrumentor:
        RedisInstrumentor().instrument()

    # Instrument HTTP client if available
    if HTTPXClientInstrumentor:
        HTTPXClientInstrumentor().instrument()


def get_tracer(name: str) -> trace.Tracer:
    """Get a tracer for manual instrumentation.

    Args:
        name: Name of the tracer (usually __name__)

    Returns:
        OpenTelemetry tracer
    """
    return trace.get_tracer(name)


def get_meter(name: str) -> metrics.Meter:
    """Get a meter for manual metrics.

    Args:
        name: Name of the meter (usually __name__)

    Returns:
        OpenTelemetry meter
    """
    return metrics.get_meter(name)
