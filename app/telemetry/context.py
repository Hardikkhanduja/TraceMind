from opentelemetry.propagate import inject, extract
from opentelemetry.context import attach, detach


def inject_trace_context() -> dict[str, str]:
    carrier: dict[str, str] = {}
    inject(carrier)
    return carrier


def attach_trace_context(carrier: dict[str, str]):
    ctx = extract(carrier)
    token = attach(ctx)
    return token


def detach_trace_context(token):
    detach(token)