import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score

# Carregar e ordenar os dados
df_base = pd.read_csv("../dataset/dengue_manaus_limpo.csv")
df_base = df_base.sort_values("SE").reset_index(drop=True)
df_base["semana_ano"] = df_base["SE"] % 100

# Testar diferentes valores de atraso (lag) e comparar
print("Testando diferentes valores de lag:\n")

for lag in [2, 3, 4, 5, 6, 8]:
    # Trabalhar com uma cópia dos dados para cada teste
    df = df_base.copy()
    df["temp_lag"] = df["tempmed"].shift(lag)
    df["umid_lag"] = df["umidmed"].shift(lag)
    df = df.dropna()

    features = ["tempmin", "tempmed", "tempmax", "umidmin", "umidmed", "umidmax", "semana_ano", "temp_lag", "umid_lag"]
    X = df[features]
    y = df["casos"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    modelo = RandomForestRegressor(n_estimators=100, random_state=42)
    modelo.fit(X_train, y_train)
    r2 = r2_score(y_test, modelo.predict(X_test))

    print(f"Lag de {lag} semanas -> R2: {r2:.3f}")