import pandas as pd
import os
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score

print("Carregando dataset histórico de 81 semanas para o treino da IA...")

# 1. Carregar o dataset real da pasta de artefatos
caminho_dados = os.path.join('..', 'artefatos', 'dados_clima_dengue.csv')
df = pd.read_csv(caminho_dados)

# 2. Separar variáveis explicativas (X) e a variável alvo (y)
X = df[['chuva_mm', 'umidade_pct', 'temp_c']]
y = df['casos_dengue']

# 3. Treinar o modelo de Inteligência Artificial (Random Forest)
print("Treinando Random Forest Regressor com 100 árvores de decisão...")
modelo = RandomForestRegressor(n_estimators=100, max_depth=6, random_state=42)
modelo.fit(X, y)

# Avaliação da acurácia do modelo
score = r2_score(y, modelo.predict(X))
print(f"Inteligência Artificial treinada com sucesso! (Precisão R² na base histórica: {score:.2f})\n")

# 4. Função limpa de previsão para o sistema
def prever_surto(chuva, umidade, temp):
    entrada = pd.DataFrame([[chuva, umidade, temp]], 
                           columns=['chuva_mm', 'umidade_pct', 'temp_c'])
    previsao = modelo.predict(entrada)[0]
    return int(previsao)



print("="*60)
print("="*60)

# Cenário 1: O Surto Crítico (Padrão de muita chuva e calor na Zona Leste/Manaus)
c1_chuva, c1_umid, c1_temp = 145.0, 91.0, 31.5
casos_critico = prever_surto(c1_chuva, c1_umid, c1_temp)
print(f"\n[CENÁRIO 1: ALERTA CRÍTICO]")
print(f"Parâmetros de Entrada: Chuva = {c1_chuva}mm | Umidade = {c1_umid}% | Temp = {c1_temp}°C")
print(f"Projeção Oficial da IA: {casos_critico:,} casos previstos para as próximas semanas.")
print(f"Ação Sugerida: Acionar semáforo VERMELHO e enviar fumacê para áreas de risco.")

# Cenário 2: Período Controlado (Para demonstrar a IA mudando ao vivo se o avaliador pedir)
c2_chuva, c2_umid, c2_temp = 25.0, 70.0, 27.0
casos_seguro = prever_surto(c2_chuva, c2_umid, c2_temp)
print(f"\n[CENÁRIO 2: PERÍODO CONTROLADO / SEGURO]")
print(f"Parâmetros de Entrada: Chuva = {c2_chuva}mm | Umidade = {c2_umid}% | Temp = {c2_temp}°C")
print(f"Projeção Oficial da IA: {casos_seguro:,} casos previstos para as próximas semanas.")
print(f"Ação Sugerida: Acionar semáforo VERDE. Monitoramento padrão da Defesa Civil.\n")
print("="*60)