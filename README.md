# PrevDengue

Sistema inteligente de apoio à tomada de decisão para previsão de surtos de dengue baseado em análise preditiva e variáveis meteorológicas. Desenvolvido como protótipo acadêmico para o ecossistema de monitoramento epidemiológico em Manaus, Amazonas.
---

# Visão Geral

O **PrevDengue** tem como objetivo auxiliar gestores públicos na prevenção de surtos de dengue por meio de modelos preditivos treinados com dados históricos do **SINAN (Sistema de Informação de Agravos de Notificação)** e informações meteorológicas.

A plataforma utiliza algoritmos de aprendizado de máquina para estimar a quantidade de notificações de dengue nas semanas epidemiológicas subsequentes, permitindo um planejamento antecipado de ações como:

- Controle vetorial;
- Alocação de equipes de campo;
- Planejamento de recursos hospitalares;
- Operações de fumacê;
- Campanhas preventivas.

A arquitetura separa o processamento de Inteligência Artificial da interface de visualização, proporcionando maior organização, escalabilidade e facilidade de manutenção.

---

# Contexto do Projeto

Este projeto foi desenvolvido durante o programa **Rocket de Férias** da **FPFtech Escola Tecnológica**, no contexto do Hackathon e Demo Day. O objetivo foi construir um MVP funcional aplicando técnicas de Ciência de Dados, Machine Learning e Desenvolvimento Web para apoiar a tomada de decisão na saúde pública.

---

# Funcionalidades

- Previsão de casos de dengue utilizando Random Forest Regressor;
- Integração entre dados epidemiológicos e meteorológicos;
- Dashboard web para visualização dos resultados;
- API REST desenvolvida em Flask;
- Geração de gráficos estatísticos;
- Geração de relatórios em PDF;
- Visualização de indicadores e nível de risco.

---

# Arquitetura

## Fluxo Geral da Solução

```mermaid
graph LR
    A[Dados SINAN e Meteorológicos]
    --> B[Pré-processamento]

    B --> C[Modelo Random Forest]

    C --> D[API Flask]

    D --> E[Dashboard Web]

    E --> F[Semáforo de Alerta para Defesa Civil]
```

---

## Diagrama de Sequência

O diagrama abaixo apresenta o fluxo completo de comunicação entre o dashboard, a API e o modelo de Machine Learning durante uma previsão.

<p align="center">
    <img src="docs/Diagrama-Sequencia.png" alt="Diagrama de Sequência" width="900">
</p>

---

## Fluxo da Aplicação

```text
Usuário
    │
    ▼
Dashboard Web
    │
    ▼
Requisição HTTP
    │
    ▼
API Flask
    │
    ▼
Pré-processamento
    │
    ▼
Random Forest Regressor
    │
    ▼
Predição
    │
    ▼
Dashboard + Relatório
```

---

# Tecnologias Utilizadas

## Back-end

- Python
- Flask
- Flask-CORS
- Pandas
- NumPy
- Scikit-Learn

## Modelo de Machine Learning

- Random Forest Regressor

## Front-end

- HTML5
- CSS3
- JavaScript (ES6+)
- Chart.js

## Relatórios

- jsPDF

---

# Metodologia de Machine Learning e Ciência de Dados

O núcleo preditivo do PrevDengue emprega algoritmos de aprendizado supervisionado para mapear a correlação não linear entre as variáveis meteorológicas e a incidência epidemiológica de dengue.

- **Algoritmo Utilizado:** Random Forest Regressor (scikit-learn), escolhido por sua robustez contra overfitting, capacidade de lidar com interações complexas entre variáveis climáticas e elevada capacidade de generalização.

- **Treinamento e Inferência:** O modelo é alimentado dinamicamente com dados históricos provenientes do SINAN e informações climáticas, realizando o treinamento durante a inicialização da API Flask e executando previsões sob demanda.

- **Validação e Métricas:** O desempenho do modelo foi validado estatisticamente, alcançando um coeficiente de determinação **R² = 0,89**, demonstrando elevada capacidade preditiva para apoio à tomada de decisão.

---

# Variáveis Climáticas Utilizadas

O modelo considera três fatores fundamentais para o desenvolvimento do vetor *Aedes aegypti*.

## Volume de Chuva (mm)

A precipitação influencia diretamente a formação de criadouros e o acúmulo de água parada.

## Umidade Relativa (%)

Afeta a sobrevivência, longevidade e atividade do mosquito adulto.

## Temperatura Média (°C)

Interfere no metabolismo do vetor, acelerando seu ciclo biológico e favorecendo a disseminação do vírus.

---

# Estrutura do Projeto

```text
PREVDENGUE-MACHINELEARNING/
│
├── backend/
│   ├── artefatos/
│   │   ├── dados_clima_dengue.csv
│   │   └── grafico_dengue.png
│   │
│   ├── dataset/
│   │   ├── DENGBR25.csv
│   │   └── DENGBR26.csv
│   │
│   └── scripts/
│       ├── api.py
│       ├── gerar_grafico.py
│       ├── modelo_preditivo.py
│       └── processar_sinan.py
│
├── docs/
│   └── Diagrama-Sequencia.png
│
├── frontend/
│   ├── index.html
│   ├── script.js
│   └── style.css
│
├── requirements.txt
├── .gitignore
└── README.md
```

---

# Como Executar

## 1. Clonar o repositório

```bash
git clone https://github.com/seu-usuario/PREVDENGUE-MACHINELEARNING.git

cd PREVDENGUE-MACHINELEARNING
```

---

## 2. Instalar as dependências

```bash
pip install -r requirements.txt
```

Caso deseje instalar manualmente:

```bash
pip install flask flask-cors pandas numpy scikit-learn matplotlib
```

---

## 3. Executar a API

```bash
cd backend/scripts

python api.py
```

A API será iniciada em:

```
http://127.0.0.1:5000/prever
```

Durante a inicialização, o sistema:

- Carrega os datasets históricos;
- Realiza o pré-processamento dos dados;
- Treina automaticamente o modelo Random Forest;
- Disponibiliza o endpoint para previsões.

---

## 4. Executar o Front-end

Abra o arquivo:

```text
frontend/index.html
```

ou utilize o **Live Server** do Visual Studio Code.

---

# Organização dos Componentes

| Diretório | Descrição |
|-----------|-----------|
| `backend/dataset` | Bases de dados originais do SINAN |
| `backend/artefatos` | Dataset tratado e gráficos gerados |
| `backend/scripts` | Processamento, treinamento e API |
| `frontend` | Dashboard web |
| `docs` | Diagramas e documentação do projeto |

---

# Modelo de Machine Learning

O sistema utiliza um modelo de regressão baseado em **Random Forest**, treinado com registros históricos provenientes do SINAN combinados a informações meteorológicas.

## Variáveis Climáticas Analisadas

O modelo preditivo fundamenta-se nos três principais fatores meteorológicos que regem o ciclo biológico do vetor *Aedes aegypti*:

1. **Volume de Chuva (mm):** Precipitação semanal que fomenta a criação de criadouros e reservatórios de água parada para desova e eclosão de larvas.
2. **Umidade Relativa (%):** Concentração de vapor d'água no ar que impacta diretamente a taxa de sobrevivência, longevidade e o raio de atividade do vetor adulto.
3. **Temperatura Média (Celsius):** Variável térmica que acelera o metabolismo do inseto, reduz o tempo de incubação extrínseca do vírus e encurta o ciclo de maturação de ovo a mosquito adulto.


## Saída do Modelo

- Quantidade prevista de notificações de dengue para semanas epidemiológicas futuras.

---

# Objetivo

Demonstrar como técnicas de Ciência de Dados, Machine Learning e Engenharia de Software podem apoiar a tomada de decisão na saúde pública por meio da previsão de surtos epidemiológicos e do planejamento preventivo baseado em evidências.

---

# Autoria

Projeto desenvolvido durante o programa **Rocket de Férias** da **FPFtech Escola Tecnológica**, demonstrando competências em:

- Engenharia de Software;
- Ciência de Dados;
- Machine Learning;
- Desenvolvimento Web Full Stack;
- Desenvolvimento de APIs REST;
- Visualização de Dados.

---

# Licença

Este projeto foi desenvolvido para fins acadêmicos e de demonstração tecnológica.
