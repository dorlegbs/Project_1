# ============================================================
# 🚨 ALERTA DE CRISE DE MARCA — VERSÃO PROFISSIONAL
# Python + Streamlit + NewsAPI + Telegram Bot
# Usando python-telegram-bot (melhor que telepot)
# ============================================================

import streamlit as st
import requests
import time
from datetime import datetime, timedelta

# ============================================================
# 🔧 O QUE VOCÊ PRECISA SUBSTITUIR
# ============================================================

# 1. Sua chave da NewsAPI
NEWS_API_KEY = "c5a9421e78db4a1ea44f579ab3c03ee3"

# 2. Token do seu Bot do Telegram
TELEGRAM_BOT_TOKEN = "8619653628:AAEfZ70FPAkUvDFb7WiYs8miLHx6zMctZcM"

# 3. Seu Chat ID do Telegram
CHAT_ID = "5936758960"

# ============================================================
# 🤖 CONFIGURAÇÃO DO BOT
# ============================================================


# ============================================================
# 📰 FUNÇÃO PARA BUSCAR MENÇÕES
# ============================================================

def buscar_mencoes(marca):
    """
    Busca quantas notícias citaram a marca
    na última 1 hora
    """

    uma_hora_atras = (
        datetime.now() - timedelta(hours=1)
    ).strftime("%Y-%m-%dT%H:%M:%S")

    url = (
        f"https://newsapi.org/v2/everything?"
        f"q={marca}"
        f"&from={uma_hora_atras}"
        f"&sortBy=publishedAt"
        f"&language=pt"
        f"&apiKey={NEWS_API_KEY}"
    )

    try:
        response = requests.get(url)
        data = response.json()

        if data["status"] != "ok":
            return 0

        return data["totalResults"]

    except:
        return 0


# ============================================================
# 📲 FUNÇÃO PARA ENVIAR ALERTA
# ============================================================

def enviar_alerta(marca, aumento):
    """
    Envia alerta no Telegram
    """

    mensagem = (
        f"⚠️ ALERTA DE CRISE DE MARCA\n\n"
        f"A marca {marca} teve aumento de "
        f"{aumento}% nas menções na última hora.\n\n"
        f"Possível crise de imagem em andamento."
    )

    try:
        bot.send_message(
            chat_id=CHAT_ID,
            text=mensagem
        )
    except:
        pass


# ============================================================
# 🔍 FUNÇÃO DE MONITORAMENTO
# ============================================================

def verificar_crise(marca, limite_alerta):
    """
    Verifica se houve pico de menções
    """

    mencoes_anterior = buscar_mencoes(marca)

    # tempo curto para teste
    # depois você pode trocar para 3600 (1 hora)
    time.sleep(10)

    mencoes_atual = buscar_mencoes(marca)

    if mencoes_anterior == 0:
        return "Sem dados suficientes para análise."

    aumento = int(
        ((mencoes_atual - mencoes_anterior)
         / mencoes_anterior) * 100
    )

    if aumento >= limite_alerta:
        enviar_alerta(marca, aumento)
        return f"⚠️ Alerta enviado! Pico de {aumento}% detectado."

    return f"Monitoramento normal. Variação: {aumento}%"


# ============================================================
# 💻 INTERFACE STREAMLIT
# ============================================================

st.set_page_config(
    page_title="Brand Watch Pro",
    page_icon="🚨",
    layout="centered"
)

st.title("🚨 Alerta de Crise de Marca")
st.subheader("Monitoramento profissional de reputação")

st.markdown("---")

# ============================================================
# INPUT DO USUÁRIO
# ============================================================

marca = st.text_input(
    "Digite a marca que deseja monitorar:",
    value="Nike",
    placeholder="Ex: Adidas, Coca-Cola, Apple"
)

limite_alerta = st.number_input(
    "Defina o percentual mínimo para disparar alerta (%)",
    min_value=50,
    max_value=1000,
    value=200,
    step=50
)

st.write(f"Marca monitorada: {marca}")
st.write(f"Limite de alerta: {limite_alerta}%")

st.markdown("---")

# ============================================================
# BOTÃO PRINCIPAL
# ============================================================

if st.button("Iniciar Monitoramento"):

    if not marca:
        st.warning("Digite uma marca.")
    else:
        with st.spinner("Monitorando menções..."):

            resultado = verificar_crise(
                marca,
                limite_alerta
            )

            st.success("Monitoramento concluído")
            st.write(resultado)

            st.info(
                "Se houver pico de menções, "
                "o alerta será enviado no Telegram."
            )



