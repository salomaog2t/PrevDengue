# PrevDengue

Sistema inteligente de apoio à tomada de decisão para previsão de surtos de dengue baseado em análise preditiva e variáveis meteorológicas. Desenvolvido como protótipo acadêmico para o ecossistema de monitoramento epidemiológico em Manaus, Amazonas.

## Visão Geral

O PrevDengue atua de forma preventiva na saúde pública. Utilizando modelos de regressão de aprendizado de máquina treinados sobre séries históricas do SINAN (Sistema de Informação de Agravos de Notificação), a plataforma cruza dados climáticos para estimar o volume de notificações de dengue nas semanas epidemiológicas subsequentes. 

A arquitetura separa rigorosamente o processamento preditivo (back-end em Python) da interface de visualização operacional (front-end web), permitindo que gestores públicos dimensionem recursos logísticos e ações de campo (como mutirões de controle vetorial e alocação de fumacê).

## Arquitetura do Sistema

- **Back-end (API REST):** Desenvolvido em Python com Flask e Flask-CORS. Utiliza o algoritmo `Random Forest Regressor` da biblioteca scikit-learn para processamento estatístico e inferência baseada nas variáveis meteorológicas.
- **Front-end:** Interface web moderna construída com HTML5, CSS3 estruturado com variáveis customizadas, JavaScript modular (padrão ES6+) e gráficos interativos via `Chart.js`. Conta com geração automatizada de relatórios executivos em PDF utilizando a biblioteca `jsPDF`.

## Variáveis Climáticas Analisadas

O modelo preditivo fundamenta-se nos três principais fatores meteorológicos que regem o ciclo biológico do vetor *Aedes aegypti*:

1. **Volume de Chuva (mm):** Precipitação semanal que fomenta a criação de criadouros e reservatórios de água parada para desova e eclosão de larvas.
2. **Umidade Relativa (%):** Concentração de vapor d'água no ar que impacta diretamente a taxa de sobrevivência, longevidade e o raio de atividade do vetor adulto.
3. **Temperatura Média (Celsius):** Variável térmica que acelera o metabolismo do inseto, reduz o tempo de incubação extrínseca do vírus e encurta o ciclo de maturação de ovo a mosquito adulto.

## Estrutura do Repositório

```text
PrevDengue/
│
├── api/                  # Servidor Flask e rotas de inferência da IA
│   └── api.py
│
├── artefatos/            # Datasets históricos limpos e modelos serializados
│   └── dados_clima_dengue.csv
│
├── src/ ou raiz/         # Interface web do painel de monitoramento
│   ├── index.html
│   ├── style.css
│   └── script.js
│
└── README.md
```

## Como Executar o Projeto

### 1. Requisitos e Dependências
Certifique-se de ter o Python instalado em sua máquina. Instale os pacotes necessários executando o comando no terminal:
```bash
pip install flask flask-cors pandas scikit-learn
```

### 2. Executando o Servidor de Inteligência Artificial (Back-end)
Navegue até o diretório da API e inicie o servidor Flask:
```bash
python api.py
```
O servidor será inicializado na porta `5000` em `http://127.0.0.1:5000/prever`, carregando o dataset histórico e treinando as 100 árvores de decisão do modelo preditivo.

### 3. Acessando a Interface Web (Front-end)
Abra o arquivo `index.html` diretamente em seu navegador web de preferência ou utilize uma extensão de servidor local (como o Live Server do VS Code) para interagir com o painel de monitoramento.

## Autoria

Protótipo desenvolvido no âmbito acadêmico para demonstração de projetos aplicados em engenharia de software e inteligência artificial preditiva.
