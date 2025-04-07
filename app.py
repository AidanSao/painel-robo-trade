import streamlit as st
import yfinance as yf
import matplotlib.pyplot as plt

st.title("Painel Robô de Trade com Médias Móveis")

ticker = st.text_input("Código da Ação", "AAPL")
ma_curta = st.slider("Média Móvel Curta", 5, 30, 20)
ma_longa = st.slider("Média Móvel Longa", 30, 200, 50)

if ticker:
    dados = yf.download(ticker, start="2022-01-01")
    dados['MA_Curta'] = dados['Close'].rolling(ma_curta).mean()
    dados['MA_Longa'] = dados['Close'].rolling(ma_longa).mean()

    st.line_chart(dados[['Close', 'MA_Curta', 'MA_Longa']])

    ultimo_sinal = "SEGURAR"
    if dados['MA_Curta'].iloc[-1] > dados['MA_Longa'].iloc[-1]:
        ultimo_sinal = "COMPRA"
    elif dados['MA_Curta'].iloc[-1] < dados['MA_Longa'].iloc[-1]:
        ultimo_sinal = "VENDA"

    st.markdown(f"### Sinal Atual: **{ultimo_sinal}**")
