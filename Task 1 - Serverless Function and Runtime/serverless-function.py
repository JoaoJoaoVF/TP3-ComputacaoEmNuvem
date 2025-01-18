import json
import redis

def calculate_percent_network_egress(bytes_sent: int) -> float:
    return bytes_sent / (10**6)

def calculate_percent_memory_cached(cached_memory: int, buffer_memory: int, total_memory: int) -> float:
    if total_memory == 0:
        return 0
    return ((cached_memory + buffer_memory) / total_memory) * 100

def update_cpu_moving_average(cpu_usage: dict, env: dict) -> dict:
    cpu_moving_avg = {}

    for cpu, usage in cpu_usage.items():
        history = env.get(cpu, [])
        history.append(usage)
        
        if len(history) > 12:
            history.pop(0)
        
        env[cpu] = history
        cpu_moving_avg[f"avg-{cpu}-60sec"] = sum(history) / len(history)

    return cpu_moving_avg

def handler(input: dict, context: object) -> dict:
    timestamp = input.get("timestamp")
    bytes_sent = input.get("net_io_counters_eth0-bytes_sent", 0)
    total_memory = input.get("virtual_memory-total", 1)
    cached_memory = input.get("virtual_memory-cached", 0)
    buffer_memory = input.get("virtual_memory-buffers", 0)
    cpu_usage = {key: value for key, value in input.items() if key.startswith("cpu_percent-")}

    percent_network_egress = calculate_percent_network_egress(bytes_sent)
    percent_memory_cached = calculate_percent_memory_cached(cached_memory, buffer_memory, total_memory)

    env = getattr(context, 'env', {})
    cpu_moving_avg = update_cpu_moving_average(cpu_usage, env)

    result = {
        "timestamp": timestamp,
        "percent-network-egress": percent_network_egress,
        "percent-memory-cached": percent_memory_cached,
        **cpu_moving_avg
    }

    context.env = env

    return result