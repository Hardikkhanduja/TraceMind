from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter

resource = Resource.create({
    "service.name": "tracemind-backend",
    "service.version": "1.0.0",
    "deployment.environment": "development",
})

provider = TracerProvider(
    resource=resource,
)

exporter = OTLPSpanExporter(
    endpoint="localhost:4317",
    insecure=True,
)

processor = BatchSpanProcessor(exporter)
provider.add_span_processor(processor)

trace.set_tracer_provider(provider)

tracer = trace.get_tracer("tracemind")