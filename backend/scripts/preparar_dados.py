import pandas as pd

# Carregar os dados reais de Manaus
df = pd.read_csv("../dataset/dengue_manaus_2014_2024.csv")

# Selecionar apenas as colunas que o modelo vai usar
colunas_uteis = ["data_iniSE", "SE", "casos", "tempmin", "tempmed", "tempmax", "umidmin", "umidmed", "umidmax"]
df = df[colunas_uteis]

print("Antes de limpar:", df.shape)

# Remover linhas que tenham algum valor faltante (NaN)
df = df.dropna()

print("Depois de limpar:", df.shape)

# Salvar os dados limpos em um novo arquivo
df.to_csv("../dataset/dengue_manaus_limpo.csv", index=False)
print("Dados limpos salvos com sucesso!")