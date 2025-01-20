import streamlit as st
import json
import redis
import time
import pandas as pd

# Configuração do Redis
REDIS_HOST = "192.168.121.187"  # Se estiver rodando localmente
REDIS_PORT = 6379
REDIS_KEY = "2021039654-proj3-output"

def fetch_data_from_redis():
    """Busca os dados do Redis e os converte para um dicionário."""
    try:
        redis_client = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=0, decode_responses=True)
        data = redis_client.get(REDIS_KEY)
        if data:
            return json.loads(data)
    except Exception as e:
        st.error(f"Erro ao conectar ao Redis: {e}")
    return {}

def main():
    """Dashboard principal."""
    st.set_page_config(page_title="Dashboard de Monitoramento", layout="wide")

    st.title("📊 Dashboard de Monitoramento")

    placeholder = st.empty()  # Para atualização dinâmica

    while True:
        data = fetch_data_from_redis()
        
        if data:
            with placeholder.container():
                st.subheader("📌 Última Atualização")
                st.write(f"🕒 Timestamp: {data.get('timestamp', 'N/A')}")

                # Métricas principais
                st.subheader("📡 Métricas de Rede e Memória")
                col1, col2 = st.columns(2)
                col1.metric("Percentual de Egressão de Rede", f"{data.get('percent-network-egress', 0):.2f} MB")
                col2.metric("Percentual de Memória em Cache", f"{data.get('percent-memory-cached', 0):.2f}%")

                # Dados da CPU
                st.subheader("💾 Média Móvel de CPU (60s)")
                cpu_metrics = {k: v for k, v in data.items() if k.startswith("avg-util-cpu")}
                
                if cpu_metrics:
                    df_cpu = pd.DataFrame(cpu_metrics.items(), columns=["CPU", "Uso (%)"])
                    st.table(df_cpu)
                else:
                    st.write("🔴 Nenhuma informação de CPU disponível.")

        else:
            st.warning("⚠ Nenhum dado disponível no Redis.")

        time.sleep(5)  # Atualiza os dados a cada 5 segundos

if __name__ == "__main__":
    main()
