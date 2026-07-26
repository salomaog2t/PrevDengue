import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_absolute_error

# Carregar os dados limpos de Manaus
df = pd.read_csv("../dataset/dengue_manaus_limpo.csv")

# Criar uma feature de sazonalidade: a semana do ano (1 a 52)
# A coluna SE vem como AAAASS (ex: 202501 = ano 2025, semana 01).
# Pegamos só os 2 últimos dígitos para ter a semana, ignorando o ano.
df["semana_ano"] = df["SE"] % 100

# Separar as variáveis preditoras (X) e o alvo (y)
features = ["tempmin", "tempmed", "tempmax", "umidmin", "umidmed", "umidmax", "semana_ano"]
X = df[features]
y = df["casos"]

print("Formato de X:", X.shape)
print("Formato de y:", y.shape)

# Dividir os dados em treino (80%) e teste (20%)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

print("Treino:", X_train.shape[0], "semanas")
print("Teste:", X_test.shape[0], "semanas")

# Treinar o modelo Random Forest apenas com os dados de treino
modelo = RandomForestRegressor(n_estimators=100, random_state=42)
modelo.fit(X_train, y_train)

# Avaliar o modelo nos dados de TESTE (que ele nunca viu)
previsoes = modelo.predict(X_test)
r2 = r2_score(y_test, previsoes)
mae = mean_absolute_error(y_test, previsoes)

print(f"R² no teste: {r2:.3f}")
print(f"Erro médio (MAE): {mae:.1f} casos")