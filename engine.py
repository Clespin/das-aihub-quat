import yfinance as yf
import pandas as pd
import json

# 1. Ingestão de Dados (Índice Bovespa como paciente zero)
ticker = "^BVSP" 
print(f"Buscando dados para {ticker}...")
dados = yf.download(ticker, period="1y", progress=False)

# 2. Engenharia de Dados (Cálculo de variação percentual diária)
dados['Retorno'] = dados['Close'].pct_change()

# 3. Estatística Descritiva Isolada
# Filtramos os dias de alta (ganhos) e dias de baixa (perdas)
ganhos = dados[dados['Retorno'] > 0]['Retorno']
perdas = dados[dados['Retorno'] < 0]['Retorno']

# Cálculo dos parâmetros do seu Simulador Monte Carlo
taxa_acerto = len(ganhos) / (len(ganhos) + len(perdas)) * 100
ganho_medio = ganhos.mean() * 100
perda_media = perdas.mean() * 100

resultados = {
    "ativo": ticker,
    "taxa_acerto_real": round(taxa_acerto, 2),
    "ganho_medio_real": round(ganho_medio, 2),
    "perda_media_real": round(perda_media, 2)
}

print("\n=== PARÂMETROS QUANTITATIVOS ATUALIZADOS ===")
print(json.dumps(resultados, indent=4))

# Salva o resultado em um arquivo JSON no repositório
with open('dados_mercado.json', 'w') as arquivo:
    json.dump(resultados, arquivo)
