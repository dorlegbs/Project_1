import streamlit as st
import requests
from pytrends.request import TrendReq
from datetime import datetime, timedelta

# -------------------------
# CONFIGURAÇÕES
# -------------------------

NEWS_API_KEY = "SUA_CHAVE_AQUI"

st.set_page_config(
    page_title="Radar de Hype",
    page_icon="📈",
    layout="centered"
)

st.title("📈 O Radar de Hype")
st.subheader("Descubra se um assunto ainda vale um post")

tema = st.text_input("Digite um tema:", placeholder="Ex: Inteligência Artificial")

# -------------------------
# FUNÇÃO NEWSAPI
# -------------------------

def buscar_noticias(tema):
    ontem = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")

    url = (
        f"https://newsapi.org/v2/everything?"
        f"q={tema}"
        f"&from={ontem}"
        f"&sortBy=publishedAt"
        f"&language=pt"
        f"&apiKey={NEWS_API_KEY}"
    )

    response = requests.get(url)
    data = response.json()

    if data["status"] != "ok":
        return 0, []

    total = data["totalResults"]
    artigos = data["articles"][:5]

    titulos = [artigo["title"] for artigo in artigos]

    return total, titulos

# -------------------------
# FUNÇÃO GOOGLE TRENDS
# -------------------------

def analisar_trends(tema):
    pytrends = TrendReq(hl='pt-BR', tz=360)

    pytrends.build_payload(
        [tema],
        cat=0,
        timeframe='now 7-d',
        geo='BR',
        gprop=''
    )

    dados = pytrends.interest_over_time()

    if dados.empty:
        return None

    valores = dados[tema].tolist()

    media_inicio = sum(valores[:3]) / 3
    media_final = sum(valores[-3:]) / 3

    if media_final > media_inicio:
        return "subindo"
    elif media_final < media_inicio:
        return "caindo"
    else:
        return "estável"

# -------------------------
# ANÁLISE FINAL
# -------------------------

if st.button("Analisar hype"):

    if not tema:
        st.warning("Digite um tema primeiro.")
    else:
        with st.spinner("Analisando..."):

            total_noticias, titulos = buscar_noticias(tema)
            tendencia = analisar_trends(tema)

            st.write("## Resultado")

            st.metric("📰 Notícias nas últimas 24h", total_noticias)
            st.write(f"📊 Tendência de busca: **{tendencia}**")

            if total_noticias > 50 and tendencia == "caindo":
                st.error("⚠️ O assunto está SATURADO")
            elif tendencia == "subindo":
                st.success("🚀 Ainda vale investir nesse tema")
            else:
                st.info("🤔 Tema em observação")

            st.write("## Principais manchetes")

            for titulo in titulos:
                st.write(f"- {titulo}")
