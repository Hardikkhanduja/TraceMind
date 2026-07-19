from app.graph.state import WorkflowState
from app.llm.gemini import llm
from app.telemetry.tracer import tracer
from app.services.runtime_context_services import RuntimeContextService
from pprint import pprint


def classify_issue(state: WorkflowState) -> WorkflowState:
    with tracer.start_as_current_span("classify_issue") as span:
        prompt = state["prompt"].strip().lower()

        if any(word in prompt for word in [
            "performance",
            "latency",
            "timeout",
            "slow",
            "delay"
        ]):
            category = "Performance"
        elif any(word in prompt for word in [
            "memory",
            "ram",
            "heap"
        ]):
            category = "Memory"
        elif any(word in prompt for word in [
            "database",
            "postgres",
            "sql",
            "query"
        ]):
            category = "Database"
        elif any(word in prompt for word in [
            "network",
            "api",
            "http",
            "request"
        ]):
            category = "Networking"
        else:
            category = "General"

        state["category"] = category

        span.set_attribute("issue.category", category)
        span.set_attribute("prompt.length", len(state["prompt"]))

        print(f"Issue Category: {category}")
        return state


def generate_investigation_plan(
        state: WorkflowState,
) -> WorkflowState:

    with tracer.start_as_current_span("generate_investigation_plan") as span:
        category = state["category"]

        plans = {
            "Database": """
            1. Check slow SQL queries.
            2. Review execution plans (EXPLAIN ANALYZE).
            3. Inspect database indexes.
            4. Check connection pool utilization.
            5. Review lock contention.
            """,

            "Memory": """
            1. Inspect heap usage.
            2. Monitor object growth.
            3. Detect memory leaks.
            4. Review garbage collection.
            5. Analyze process memory.
            """,

            "Networking": """
            1. Check request latency.
            2. Verify API connectivity.
            3. Inspect retries and timeouts.
            4. Review DNS resolution.
            5. Analyze network throughput.
            """,

            "Performance": """
            1. Measure API response times.
            2. Check LLM Latency.
            3. Inspect system resource usage.
            4. Review memory usage.
            5. Identify bottlenecks.
            """,

            "General": """
            1. Collect logs.
            2. Review recent deployments.
            3. Inspect workflow execution.
            4. Verify configuration.
            5. Gather additional traces.
            """
        }

        state["investigation_plan"] = plans[category].strip()

        span.set_attribute("investigation.category", category)
        span.set_attribute("plan.steps", 5)

        print(f"Investigation plan Generated for {category}")
        return state


def collect_runtime_context(
        state: WorkflowState
) -> WorkflowState:

    with tracer.start_as_current_span("collect_runtime_context") as span:
        service = RuntimeContextService()
        
        runtime_context = service.collect(
            state["category"]
        )
        
        state["system_metrics"] = runtime_context["system"]
        state["application_metrics"] = runtime_context["application"]
        
        system = runtime_context["system"]
        
        span.set_attribute(
            "runtime.context.generated",
            True
        )
        
        span.set_attribute(
            "cpu.percent",
            system["cpu_usage_percent"],
        )
        
        span.set_attribute(
            "memory.percent",
            system["memory_usage_percent"],
        )
        
        span.set_attribute(
            "disk.percent",
            system["disk_usage_percent"],
        )
        
        span.set_attribute(
            "running.processes",
            system["running_processes"],
        )
        
        span.set_attribute(
            "hostname",
            system["hostname"],
        )
        
        span.set_attribute(
            "os",
            system["os"],
        )
        
        span.set_attribute(
            "python.version",
            system["python_version"],
        )

        print("Runtime Context Collected")
        return state


def analyze_prompt(state: WorkflowState) -> WorkflowState:
    with tracer.start_as_current_span("analyze_prompt") as span:
        system_metrics = state["system_metrics"]
        application_metrics = state["application_metrics"]
        prompt = state["prompt"]
        category = state["category"]
        plan = state["investigation_plan"]

        span.set_attribute(
            "llm.model",
            "gemini-3.5-flash",
        )
        
        print("\n" + "=" * 60)
        print("SYSTEM METRICS SENT TO GEMINI")
        print("=" * 60)
        pprint(system_metrics)

        print("\n" + "=" * 60)
        print("APPLICATION METRICS SENT TO GEMINI")
        print("=" * 60)
        print(application_metrics)

        print("\n" + "=" * 60)
        print("CATEGORY")
        print(category)

        print("\n" + "=" * 60)
        print("INVESTIGATION PLAN")
        print(plan)
        print("=" * 60)
        
        llm_prompt = f"""
You are an experienced AI Site Reliability Engineer.

The issue has already been classified.

Category:
{category}

Investigation Plan:
{plan}

System Metrics:

{system_metrics}

Application Metrics:

{application_metrics}

Analyze the following production incident.

Treat the system metrics and application metrics as the **actual observed telemetry**.

If the telemetry contradicts the incident description,
explicitly mention the discrepancy instead of assuming the incident description is correct.

Base your conclusions primarily on the observed telemetry. Do not assume the deployment environment, cloud provider, developer workstation, operating system configuration, or production architecture unless explicitly supported by the provided telemetry.

Your report MUST contain exactly these sections:

1. Summary

2. Possible Root Causes

3. Investigation Steps

4. Recommended Fixes

Incident Description:

{prompt}
"""

        print("\n" + "=" * 60)
        print("PROMPT SENT TO GEMINI")
        print("=" * 60)
        print(llm_prompt)
        
        response = llm.invoke(llm_prompt)
   
        if response.content and isinstance(response.content[0], dict):
            state["analysis"] = response.content[0]["text"]
            state["final_report"] = response.content[0]["text"]

            span.set_attribute(
                "analysis.generated",
                True,
            )
        else:
            state["analysis"] = "No analysis generated."
            state["final_report"] = "No analysis generated"

            span.set_attribute(
                "analysis.generated",
                False,
            )
         
        print("Analysis generated successfully.")
        return state
