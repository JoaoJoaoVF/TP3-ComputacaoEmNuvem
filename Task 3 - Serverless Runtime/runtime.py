import os
import time
import redis
import importlib

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
REDIS_DB = int(os.getenv("REDIS_DB", 0))
redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)

handler_module = importlib.import_module("handler")
handler = getattr(handler_module, "handler")

class Context:
    def __init__(self):
        self.env = {}

context = Context()

while True:
    try:
        data = {
            "bytes_sent": float(redis_client.get("bytes_sent") or 0),
            "total_memory": float(redis_client.get("total_memory") or 1),
            "cached_memory": float(redis_client.get("cached_memory") or 0),
            "buffer_memory": float(redis_client.get("buffer_memory") or 0),
            "cpu_usage": float(redis_client.get("cpu_usage") or 0),
        }

        result = handler(data, context)

        for key, value in result.items():
            redis_client.set(key, value)
        
        print("Dados processados e armazenados com sucesso!")
    
    except Exception as e:
        print(f"Erro no runtime: {e}")
    
    time.sleep(5)  
