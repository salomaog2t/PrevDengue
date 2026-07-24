from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
import os

app = Flask(__name__)
# O CORS é obrigatório para permitir que a interface no navegador se conecte sem bloqueio de segurança
CORS(app)

print("Carregando base histórica e treinando Inteligência Artificial para a Defesa Civil...")

# 1. Carrega a base limpa dos artefatos e treina o modelo ao ligar o servidor
caminho_dados = os.path.join('..', 'artefatos', 'dados_clima_dengue.csv')

if not os.path.exists(caminho_dados):
    raise FileNotFoundError(f"❌ Erro: Arquivo não encontrado em {caminho_dados}. Rode o 'processar_sinan.py' primeiro!")

df = pd.read_csv(caminho_dados)

# Separa as variáveis climáticas (Chuva, Umidade, Temperatura) e a variável alvo (Casos)
X = df[['chuva_mm', 'umidade_pct', 'temp_c']]
y = df['casos_dengue']

# Treina o Random Forest Regressor
modelo = RandomForestRegressor(n_estimators=100, max_depth=6, random_state=42)
modelo.fit(X, y)

print("IA Treinada com Sucesso! (100 árvores de decisão processadas)")
print("Servidor PrevDengue PRONTO e aguardando o Front-end na porta 5000!")

# 2. Rota que o Front-end (script do Salomão) vai chamar ao clicar em "Calcular"
@app.route('/prever', methods=['POST'])
def prever():
    try:
        dados = request.get_json()
        
        # Recebe os valores digitados no navegador pelo usuário (ou assume valor padrão em caso de erro)
        chuva = float(dados.get('chuva', 0))
        umidade = float(dados.get('umidade', 0))
        temp = float(dados.get('temp', 0))

        # Estrutura os dados para o formato que a nossa IA espera
        entrada = pd.DataFrame([[chuva, umidade, temp]], 
                               columns=['chuva_mm', 'umidade_pct', 'temp_c'])
        
        # Realiza a previsão
        previsao = int(modelo.predict(entrada)[0])
        
        # Lógica inteligente para acionar o Semáforo da Saúde
        if previsao > 30000:
            alerta = "vermelho"
            mensagem = "SURTO EPIDEMIOLÓGICO PREVISTO! Mobilizar fumacê e agentes de endemias imediatamente para as zonas de risco."
        elif previsao > 10000:
            alerta = "amarelo"
            mensagem = "Risco Moderado. Condições climáticas altamente favoráveis à eclosão do vetor."
        else:
            alerta = "verde"
            mensagem = "Situação epidemiológica sob controle. Baixo risco de proliferação do mosquito."

        # Imprime no terminal em tempo real (Ótimo para mostrar aos juízes no Demo Day!)
        print(f"[CONSULTA AO VIVO] Chuva: {chuva}mm | Umidade: {umidade}% | Temp: {temp}°C  👉 Resultado: {previsao:,} casos ({alerta.upper()})")

        # Retorna o pacote de dados formatado para o JavaScript do HTML atualizar a tela
        return jsonify({
            'sucesso': True,
            'casos': previsao,
            'casos_formatado': f"{previsao:,}".replace(',', '.'), # Formato padrão brasileiro com ponto
            'alerta': alerta,
            'mensagem': mensagem
        })

    except Exception as e:
        print(f"Erro na requisição do Front-end: {e}")
        return jsonify({'sucesso': False, 'erro': str(e)}), 500

if __name__ == '__main__':
    # Roda em localhost com debug ativado
    app.run(host='0.0.0.0', port=5000, debug=True)