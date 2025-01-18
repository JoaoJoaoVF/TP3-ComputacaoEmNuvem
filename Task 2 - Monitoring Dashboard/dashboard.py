import streamlit as st
import redis
import json

redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)

def fetch_data_from_redis():
  key = '2021039654-proj3-output'
  data = redis_client.get(key)
  if data:
      return json.loads(data)
  return {}

def main():
  st.title("Dashboard de Monitoramento")

  data = fetch_data_from_redis()

  if data:
      st.header("Métricas de Rede e Memória")
      st.write("Percentual de Egressão de Rede:", data.get("percent-network-egress"))
      st.write("Percentual de Memória em Cache:", data.get("percent-memory-cached"))

      st.header("Média Móvel de CPU")
      cpu_keys = [key for key in data.keys() if key.startswith("avg-cpu")]
      for key in cpu_keys:
          st.write(f"{key}:", data[key])
  else:
      st.write("Nenhum dado disponível.")

if __name__ == "__main__":
  main()