# ============================================================
# 🚨 ALERTA DE CRISE DE MARCA — CÓDIGO ÚNICO
# Python + Streamlit + NewsAPI + Telegram Bot
#
# O sistema monitora menções de uma marca e envia alerta
# automático no Telegram quando detecta um pico de volume.
#
# ============================================================

import streamlit as st
import requests
import telepot
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

# 4. Nome da marca que deseja monitorar
MARCA_PADRAO = "Nike"

# 5. Percentual mínimo para disparar alerta
# Exemplo: 200 = aumento de 200%
LIMITE_ALERTA = 200

# ============================================================
# 🤖 CONFIGURAÇÃO DO BOT
# ============================================================

bot = telepot.Bot(TELEGRAM_BOT_TOKEN)

# ============================================================
# 📰 FUNÇÃO PARA BUSCAR MENÇÕES NA NEWSAPI
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
# 📲 FUNÇÃO PARA ENVIAR ALERTA NO TELEGRAM
# ============================================================

def enviar_alerta(marca, aumento):
    """
    Envia mensagem automática no Telegram
    """

    mensagem = (
        f"⚠️ ALERTA DE CRISE DE MARCA\n\n"
        f"A marca: {marca}\n"
        f"teve aumento de {aumento}% nas menções\n"
        f"na última hora.\n\n"
        f"Possível crise de imagem em andamento."
    )

    bot.sendMessage(CHAT_ID, mensagem)


# ============================================================
# 🔍 FUNÇÃO DE MONITORAMENTO
# ============================================================

def verificar_crise(marca):
    """
    Compara o volume atual com o anterior
    """

    mencoes_anterior = buscar_mencoes(marca)

    # espera alguns segundos apenas para teste
    # depois você pode trocar para 3600 (1 hora)
    time.sleep(10)

    mencoes_atual = buscar_mencoes(marca)

    if mencoes_anterior == 0:
        return "Sem dados suficientes ainda."

    aumento = int(
        ((mencoes_atual - mencoes_anterior)
         / mencoes_anterior) * 100
    )

    if aumento >= LIMITE_ALERTA:
        enviar_alerta(marca, aumento)
        return f"⚠️ Alerta enviado! Pico de {aumento}% detectado."

    return f"Monitoramento normal. Variação: {aumento}%"


# ============================================================
# 💻 INTERFACE STREAMLIT
# ============================================================

st.set_page_config(
    page_title="Brand Watch",
    page_icon="🚨",
    layout="centered"
)

st.title("🚨 Alerta de Crise de Marca")
st.subheader("Monitoramento simples de reputação")

marca = st.text_input(
    "Digite a marca que deseja monitorar:",
    value=MARCA_PADRAO
)

st.markdown("---")

if st.button("Iniciar Monitoramento"):

    if not marca:
        st.warning("Digite uma marca.")
    else:
        with st.spinner("Monitorando menções..."):

            resultado = verificar_crise(marca)

            st.success("Monitoramento concluído")
            st.write(resultado)

            st.info(
                "Se houver pico de menções, "
                "o alerta será enviado no Telegram."
            )


# ============================================================
# ▶️ COMO RODAR
# ============================================================


pip install streamlit requests telepot pandas

