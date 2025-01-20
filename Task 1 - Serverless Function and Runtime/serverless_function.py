import time

def calculate_percent_network_egress(bytes_sent: int) -> float:
    return bytes_sent / (10**6)

def calculate_percent_memory_cached(cached_memory: int, buffer_memory: int, total_memory: int) -> float:
    if total_memory == 0:
        return 0
    return ((cached_memory + buffer_memory) / total_memory) * 100

def update_cpu_moving_average(cpu_usage: dict, context: dict) -> dict:
    if "last_cpu_average" not in context["env"]:
        context["env"]["last_cpu_average"] = {cpu: [] for cpu in cpu_usage.keys()}
    
    current_time = time.time()
    cpu_moving_avg = {}

    for cpu, usage in cpu_usage.items():
        context["env"]["last_cpu_average"][cpu].append((current_time, usage))

        context["env"]["last_cpu_average"][cpu] = [
            (ts, percent) for ts, percent in context["env"]["last_cpu_average"][cpu] if current_time - ts <= 60
        ]

        avg = sum(percent for _, percent in context["env"]["last_cpu_average"][cpu]) / len(context["env"]["last_cpu_average"][cpu]) if context["env"]["last_cpu_average"][cpu] else 0
        cpu_moving_avg[f"avg-util-cpu{cpu}-60sec"] = avg

    return cpu_moving_avg

def handler(input: dict, context: dict) -> dict:
    try:
        timestamp = input.get("timestamp")
        bytes_sent = input.get("net_io_counters_eth0-bytes_sent1", 0)
        total_memory = input.get("virtual_memory-total", 1)
        cached_memory = input.get("virtual_memory-cached", 0)
        buffer_memory = input.get("virtual_memory-buffers", 0)

        cpu_usage = {key.split("-")[2]: value for key, value in input.items() if key.startswith("cpu_percent-")}

        percent_network_egress = calculate_percent_network_egress(bytes_sent)
        percent_memory_cached = calculate_percent_memory_cached(cached_memory, buffer_memory, total_memory)

        if "env" not in context:
            context["env"] = {}

        cpu_moving_avg = update_cpu_moving_average(cpu_usage, context)

        result = {
            "timestamp": timestamp,
            "percent-network-egress": percent_network_egress,
            "percent-memory-cached": percent_memory_cached,
            **cpu_moving_avg
        }

        return result
    except Exception as e:
        return {"error": str(e)}
