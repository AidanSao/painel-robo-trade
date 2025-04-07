import streamlit as st
import yfinance as yf

st.title("Painel Robô de Trade com Médias Móveis")

ticker = st.text_input("Código da Ação", "AAPL")
ma_curta = st.slider("Média Móvel Curta", 5, 30, 20)
ma_longa = st.slider("Média Móvel Longa", 30, 200, 50)

if ticker:
    dados = yf.download(ticker, start="2022-01-01")

    if dados.empty:
        st.error("Não foi possível carregar os dados. Verifique o código da ação.")
    else:
        # Verifica se 'Close' existe antes de continuar
        if 'Close' not in dados.columns:
            st.error("Os dados não contêm a coluna 'Close'.")
        else:
            # Calcula médias móveis
            dados['MA_Curta'] = dados['Close'].rolling(ma_curta).mean()
            dados['MA_Longa'] = dados['Close'].rolling(ma_longa).mean()

            # Verifica se as colunas foram criadas com sucesso
            colunas_para_grafico = []
            for col in ['Close', 'MA_Curta', 'MA_Longa']:
                if col in dados.columns:
                    colunas_para_grafico.append(col)

            if colunas_para_grafico:
                st.line_chart(dados[colunas_para_grafico])
            else:
                st.warning("Não há colunas disponíveis para exibir no gráfico.")

            # Exibe sinal apenas se os valores finais não forem NaN
            if not dados['MA_Curta'].isna().iloc[-1] and not dados['MA_Longa'].isna().iloc[-1]:
                if dados['MA_Curta'].iloc[-1] > dados['MA_Longa'].iloc[-1]:
                    st.success("Sinal Atual: COMPRA")
                elif dados['MA_Curta'].iloc[-1] < dados['MA_Longa'].iloc[-1]:
                    st.error("Sinal Atual: VENDA")
                else:
                    st.info("Sinal Atual: SEGURAR")
            else:
                st.warning("Ainda não há dados suficientes para gerar sinal.")
