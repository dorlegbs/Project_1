import streamlit as st

st.title("PIRULITOS")
st.write("SÃO DOCINHOS")

st.image("https://github.com/dorlegbs/Project_1/blob/main/pirulitos.webp?raw=true")
         
sabor = st.text_input('Digite o seu sabor preferido')
if nome:
         st.write(sabor, "é um ótimo sabor de pirulito!")
