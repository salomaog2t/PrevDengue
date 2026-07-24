import pandas as pd
import matplotlib.pyplot as plt
import os

print("Gerando gráfico de impacto epidemiológico (Chuva vs Casos)...")

# 1. Carregar os dados limpos e consolidados que geramos no processar_sinan.py
caminho_dados = os.path.join('..', 'artefatos', 'dados_clima_dengue.csv')
caminho_grafico = os.path.join('..', 'artefatos', 'grafico_dengue.png')

# Verifica se o dataset já foi gerado
if not os.path.exists(caminho_dados):
    print(f"Erro: O arquivo {caminho_dados} não foi encontrado. Rode o 'processar_sinan.py' primeiro.")
    exit()

df = pd.read_csv(caminho_dados)

# 2. Configurar o estilo Dark Mode (Estética de Dashboard de Comando)
plt.style.use('dark_background')
fig, ax1 = plt.subplots(figsize=(11, 5), dpi=300)

# Fundo cinza escuro no estilo de painel de controle
fig.patch.set_facecolor('#1a1a20')
ax1.set_facecolor('#1a1a20')

# 3. Plotar Volume de Chuva (Barras azuis no eixo esquerdo)
cor_chuva = '#00b4d8'
ax1.set_xlabel('Semanas Epidemiológicas Contínuas (2025 - 2026)', fontsize=11, fontweight='bold', labelpad=10)
ax1.set_ylabel('Volume de Chuva (mm)', color=cor_chuva, fontsize=11, fontweight='bold')

# Criando as barras de chuva
ax1.bar(df['semana'], df['chuva_mm'], color=cor_chuva, alpha=0.5, label='Chuva (mm)')
ax1.tick_params(axis='y', labelcolor=cor_chuva)
ax1.grid(False) # Remover grade para manter o visual mais limpo

# 4. Plotar Casos de Dengue (Linha vermelha no eixo direito)
ax2 = ax1.twinx() # Cria o eixo Y duplo, compartilhando o eixo X
cor_dengue = '#ff4d4d'
ax2.set_ylabel('Notificações de Dengue (SINAN)', color=cor_dengue, fontsize=11, fontweight='bold')

# Criando a linha contínua
ax2.plot(df['semana'], df['casos_dengue'], color=cor_dengue, linewidth=2.5, marker='o', markersize=3, label='Casos Confirmados')
ax2.tick_params(axis='y', labelcolor=cor_dengue)
ax2.grid(False)

# 5. Título e Acabamento Visual
plt.title('MONITORAMENTO EPIDEMIOLÓGICO: Impacto da Pluviosidade nos Casos de Dengue', 
          fontsize=12, fontweight='bold', pad=15, color='white')

# Destaque de Surto Crítico: Encontra a semana com mais casos e pinta uma faixa vermelha translúcida
semana_pico = df['casos_dengue'].idxmax() + 1
# Faixa cobrindo as 5 semanas anteriores e as 5 posteriores ao pico principal
ax1.axvspan(max(1, semana_pico - 5), min(len(df), semana_pico + 5), color='#ff4d4d', alpha=0.15)

# 6. Salvar imagem para entregar ao Front-end
plt.tight_layout()
plt.savefig(caminho_grafico, format='png', facecolor=fig.get_facecolor(), edgecolor='none')

print(f" SUCESSO! Gráfico exportado em alta resolução para a equipe de UI/UX em: '{caminho_grafico}'")