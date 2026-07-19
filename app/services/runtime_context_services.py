import platform
import socket
from datetime import datetime

import psutil


class RuntimeContextService:

    def collect(self, category: str) -> dict[str, dict]:

        virtual_memory = psutil.virtual_memory()
        disk = psutil.disk_usage("/")
        cpu = psutil.cpu_percent(interval=1)
        network = psutil.net_io_counters()

        runtime_context = {
            "system": {
                "hostname": socket.gethostname(),
                "os": platform.system(),
                "os_version": platform.version(),
                "python_version": platform.python_version(),

                "cpu_usage_percent": cpu,

                "memory_usage_percent": virtual_memory.percent,

                "memory_total_gb": round(
                    virtual_memory.total / (1024 ** 3), 2
                ),

                "memory_available_gb": round(
                    virtual_memory.available / (1024 ** 3), 2
                ),

                "disk_usage_percent": disk.percent,

                "running_processes": len(psutil.pids()),

                "boot_time": datetime.fromtimestamp(
                    psutil.boot_time()
                ).isoformat(),

                "network": {
                    "bytes_sent": network.bytes_sent,
                    "bytes_received": network.bytes_recv,
                    "packets_sent": network.packets_sent,
                    "packets_received": network.packets_recv,
                },
            },

            "application": {}
        }

        if category == "Performance":
            runtime_context["application"] = {
                "api_latency": "Unknown",
                "llm_latency": "Unknown",
                "concurrent_requests": "Unknown"
            }

        elif category == "Database":
            runtime_context["application"] = {
                "database": "PostgreSQL",
                "slow_queries": "Unknown",
                "query_latency": "Unknown",
                "connection_pool": "Unknown"
            }

        elif category == "Memory":
            runtime_context["application"] = {
                "heap_usage": "Unknown",
                "garbage_collection": "Unknown"
            }

        elif category == "Networking":
            runtime_context["application"] = {
                "http_errors": "Unknown",
                "network_latency": "Unknown"
            }
            
        print("\n" + "=" * 60)
        print("RUNTIME CONTEXT GENERATED")
        print("=" * 60)
        print(runtime_context)
        print("=" * 60)

        return runtime_context