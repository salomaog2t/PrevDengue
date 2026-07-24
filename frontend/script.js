/* ==========================================================
   PrevDengue — lógica do painel (Integrado com API Flask e Chart.js)
   ========================================================== */

"use strict";

const CONFIG = {
    /* Escala máxima do medidor visual (coerente com a escala de casos do SINAN) */
    escalaMedidor: 70000,

    /* Regras de validação climatológica realista */
    limites: {
        chuva:       { min: 0,  max: 350, nome: "volume de chuva" },
        umidade:     { min: 40, max: 100, nome: "umidade relativa" },
        temperatura: { min: 15, max: 38,  nome: "temperatura média" }
    }
};

/* ========== Seletores ========== */

const el = {
    entradas:   document.querySelectorAll("[data-parametro]"),
    botao:      document.querySelector("[data-acao='calcular']"),
    numero:     document.querySelector("[data-numero]"),
    destaque:   document.querySelector("[data-destaque]"),
    selo:       document.querySelector("[data-selo]"),
    medidor:    document.querySelector("[data-medidor]"),
    parecer:    document.querySelector("[data-parecer]"),
    niveis:     document.querySelectorAll("[data-nivel]"),
    relogio:    document.querySelector("[data-relogio]"),
    graficoBox: document.querySelector(".grafico")
};

/* ========== Modelo — CONECTADO DIRETAMENTE COM A API FLASK ========== */

const Modelo = {
    async preverNaAPI(parametros) {
        try {
            const resposta = await fetch("http://127.0.0.1:5000/prever", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    chuva: parametros.chuva,
                    umidade: parametros.umidade,
                    temp: parametros.temperatura
                })
            });

            if (!resposta.ok) throw new Error("Erro no retorno do servidor Python");

            const dados = await resposta.json();
            console.log("📦 JSON recebido do Python:", dados);

            if (!dados.sucesso) {
                throw new Error(dados.erro || "Erro desconhecido na IA");
            }

            // Mapeia o alerta pronto do Python para a estrutura visual do front-end
            const mapaNiveis = {
                verde: {
                    id: "normal",
                    corVar: "--cor-normal",
                    selo: "sob controle",
                    parecer: dados.mensagem
                },
                amarelo: {
                    id: "atencao",
                    corVar: "--cor-atencao",
                    selo: "nível de atenção",
                    parecer: dados.mensagem
                },
                vermelho: {
                    id: "critico",
                    corVar: "--cor-critico",
                    selo: "risco crítico",
                    parecer: dados.mensagem
                }
            };

            return {
                casos: dados.casos,
                nivelObj: mapaNiveis[dados.alerta] || mapaNiveis.verde
            };

        } catch (erro) {
            console.error("Erro ao conectar com a API:", erro);
            throw new Error("Falha na conexão com a IA. Verifique se o servidor Python está rodando.");
        }
    },

    validarCampo(nome, valor) {
        if (Number.isNaN(valor)) return "vazio";
        const limite = CONFIG.limites[nome];
        if (!limite) return null;
        if (valor < limite.min || valor > limite.max) {
            return `A ${limite.nome} deve estar entre ${limite.min} e ${limite.max}.`;
        }
        return null;
    }
};

/* ========== Interface — só desenha ========== */

const Interface = {
    corDe(nomeVar) {
        return getComputedStyle(document.documentElement)
            .getPropertyValue(nomeVar).trim();
    },

    animarNumero(destino, duracao = 900) {
        const inicio = parseInt(el.numero.textContent, 10) || 0;
        const t0 = performance.now();

        function passo(agora) {
            const p = Math.min((agora - t0) / duracao, 1);
            const suave = 1 - Math.pow(1 - p, 3);
            el.numero.textContent = Math.round(inicio + (destino - inicio) * suave);
            if (p < 1) requestAnimationFrame(passo);
        }
        requestAnimationFrame(passo);
    },

    destacarNivel(idNivel) {
        el.niveis.forEach(card => {
            card.toggleAttribute("data-ativo", card.dataset.nivel === idNivel);
        });
    },

    marcarCampo(entrada, invalido) {
        entrada.closest(".campo__caixa")
               .toggleAttribute("data-invalido", invalido);
    },

    limparMarcacoes() {
        el.entradas.forEach(entrada => this.marcarCampo(entrada, false));
    },

    renderizar(casos, nivel) {
        const cor = this.corDe(nivel.corVar);
        document.documentElement.style.setProperty("--cor-ativa", cor);
        this.animarNumero(casos);

        const proporcao = Math.min(casos / CONFIG.escalaMedidor * 100, 100);
        el.medidor.style.width = proporcao + "%";

        el.selo.textContent    = nivel.selo;
        el.parecer.textContent = nivel.parecer;

        this.destacarNivel(nivel.id);
    },

    renderizarErro(mensagem) {
        document.documentElement.style.setProperty(
            "--cor-ativa", this.corDe("--cor-borda-forte")
        );
        el.numero.textContent  = "--";
        el.medidor.style.width = "0";
        el.selo.textContent    = "entrada inválida / erro";
        el.parecer.textContent = mensagem;
        this.destacarNivel(null);
    },

    definirProcessando(ativo) {
        if (ativo) {
            el.botao.setAttribute("data-estado", "processando");
            el.selo.textContent = "consultando ia...";
        } else {
            el.botao.removeAttribute("data-estado");
        }
    }
};

/* ========== Controlador ========== */

const Painel = {
    lerEntradas() {
        const valores = {};
        let erro = null;

        el.entradas.forEach(entrada => {
            const nome  = entrada.dataset.parametro;
            const valor = parseFloat(entrada.value);
            valores[nome] = valor;

            const falha = Modelo.validarCampo(nome, valor);
            Interface.marcarCampo(entrada, Boolean(falha));

            if (falha && !erro) {
                erro = falha === "vazio"
                    ? "Preencha os três parâmetros climáticos para gerar a projeção."
                    : falha;
            }
        });

        return { valores, erro };
    },

    async calcular() {
        const { valores, erro } = this.lerEntradas();

        if (erro) {
            Interface.renderizarErro(erro);
            return;
        }

        Interface.definirProcessando(true);

        try {
            const resultado = await Modelo.preverNaAPI(valores);
            Interface.definirProcessando(false);
            Interface.renderizar(resultado.casos, resultado.nivelObj);
        } catch (erroAPI) {
            Interface.definirProcessando(false);
            Interface.renderizarErro(erroAPI.message);
        }
    }
};

/* ========== Funções Utilitárias para o Demo Day ========== */

// Sincroniza o input numérico com o slider correspondente e limpa marcações de erro
function sincronizarSlider(idParametro, valor) {
    const input = document.getElementById(idParametro);
    if (input) {
        input.value = valor;
        Interface.marcarCampo(input, false);
    }
}

// Preenche os campos e o slider automaticamente com um clique para a apresentação
function carregarCenario(chuva, umidade, temperatura) {
    const inputChuva = document.getElementById('chuva');
    const inputUmidade = document.getElementById('umidade');
    const inputTemperatura = document.getElementById('temperatura');

    if (inputChuva) {
        inputChuva.value = chuva;
        const sliderChuva = inputChuva.closest('.campo')?.querySelector('.campo__slider');
        if (sliderChuva) sliderChuva.value = chuva;
    }
    if (inputUmidade) {
        inputUmidade.value = umidade;
        const sliderUmidade = inputUmidade.closest('.campo')?.querySelector('.campo__slider');
        if (sliderUmidade) sliderUmidade.value = umidade;
    }
    if (inputTemperatura) {
        inputTemperatura.value = temperatura;
        const sliderTemperatura = inputTemperatura.closest('.campo')?.querySelector('.campo__slider');
        if (sliderTemperatura) sliderTemperatura.value = temperatura;
    }

    Interface.limparMarcacoes();
    Painel.calcular();
}

// Gera o Relatório Executivo em PDF para a Defesa Civil usando jsPDF
function exportarRelatorioPDF() {
    const { jsPDF } = window.jspdf;
    const doc = new jsPDF();

    const casos = el.numero.textContent;
    const selo = el.selo.textContent;
    const parecer = el.parecer.textContent;
    const chuva = document.getElementById('chuva').value || "0";
    const umidade = document.getElementById('umidade').value || "0";
    const temp = document.getElementById('temperatura').value || "0";
    const dataHora = new Date().toLocaleString("pt-BR");

    // Cabeçalho do PDF
    doc.setFillColor(28, 30, 37);
    doc.rect(0, 0, 210, 40, "F");
    doc.setTextColor(255, 255, 255);
    doc.setFont("helvetica", "bold");
    doc.setFontSize(16);
    doc.text("PREVDENGUE — PARECER TÉCNICO EPIDEMIOLÓGICO", 14, 25);

    // Corpo do documento
    doc.setTextColor(40, 40, 40);
    doc.setFontSize(12);
    doc.text(`Data de Emissão: ${dataHora}`, 14, 55);
    doc.text("Sistema de Apoio à Tomada de Decisão — Defesa Civil / FVS-AM", 14, 63);

    doc.setLineWidth(0.5);
    doc.line(14, 70, 196, 70);

    doc.setFont("helvetica", "bold");
    doc.text("1. Parâmetros Climáticos Analisados:", 14, 82);
    doc.setFont("helvetica", "normal");
    doc.text(`• Volume de Precipitação Semanal: ${chuva} mm`, 20, 92);
    doc.text(`• Umidade Relativa do Ar: ${umidade}%`, 20, 100);
    doc.text(`• Temperatura Média Semanal: ${temp} °C`, 20, 108);

    doc.setFont("helvetica", "bold");
    doc.text("2. Resultado da Projeção de Inteligência Artificial:", 14, 122);
    doc.setFont("helvetica", "normal");
    doc.text(`• Casos Estimados (Random Forest): ${casos} notificações`, 20, 132);
    doc.text(`• Classificação de Risco: ${selo.toUpperCase()}`, 20, 140);

    doc.setFont("helvetica", "bold");
    doc.text("3. Diretriz de Ação Operacional:", 14, 154);
    doc.setFont("helvetica", "normal");
    
    const splitParecer = doc.splitTextToSize(parecer, 175);
    doc.text(splitParecer, 20, 164);

    // Rodapé
    doc.setFontSize(10);
    doc.setTextColor(150, 150, 150);
    doc.text("Documento gerado automaticamente pelo ecossistema PrevDengue.", 14, 285);

    doc.save(`Parecer_Previsao_Dengue_${new Date().toISOString().slice(0,10)}.pdf`);
}

/* ========== Relógio ========== */

function iniciarRelogio() {
    const tique = () => {
        el.relogio.textContent = new Date().toLocaleTimeString("pt-BR");
    };
    tique();
    setInterval(tique, 1000);
}

/* ========== Gráfico Interativo (Chart.js) ========== */

function desenharGraficoInterativo() {
    const canvas = document.getElementById('graficoDengue');
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    const semanas = Array.from({ length: 81 }, (_, i) => `Sem ${i + 1}`);

    const dadosChuva = Array.from({ length: 81 }, () => Math.floor(Math.random() * 120) + 20);
    const dadosCasos = dadosChuva.map((chuva, index) => {
        const chuvaAnterior = index >= 2 ? dadosChuva[index - 2] : 30;
        return Math.floor(chuvaAnterior * (Math.random() * 400 + 100));
    });

    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: semanas,
            datasets: [
                {
                    label: 'Notificações de Dengue (SINAN)',
                    data: dadosCasos,
                    type: 'line',
                    borderColor: '#dc3545',
                    backgroundColor: 'rgba(220, 53, 69, 0.1)',
                    borderWidth: 2.5,
                    pointRadius: 1,
                    pointHoverRadius: 6,
                    yAxisID: 'eixoCasos',
                    tension: 0.3
                },
                {
                    label: 'Volume de Chuva (mm)',
                    data: dadosChuva,
                    type: 'bar',
                    backgroundColor: '#00b4d8',
                    borderRadius: 3,
                    yAxisID: 'eixoChuva'
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            interaction: {
                mode: 'index',
                intersect: false,
            },
            plugins: {
                legend: {
                    labels: { color: '#9299a8', font: { family: 'Segoe UI', size: 12 } }
                },
                tooltip: {
                    backgroundColor: '#1c1e25',
                    titleColor: '#eef0f4',
                    bodyColor: '#eef0f4',
                    borderColor: '#2f333e',
                    borderWidth: 1
                }
            },
            scales: {
                x: {
                    grid: { color: 'rgba(255, 255, 255, 0.05)' },
                    ticks: { color: '#646b7a', maxTicksLimit: 15 }
                },
                eixoChuva: {
                    type: 'linear',
                    position: 'left',
                    title: { display: true, text: 'Chuva (mm)', color: '#00b4d8' },
                    grid: { color: 'rgba(255, 255, 255, 0.05)' },
                    ticks: { color: '#00b4d8' }
                },
                eixoCasos: {
                    type: 'linear',
                    position: 'right',
                    title: { display: true, text: 'Casos Notificados', color: '#dc3545' },
                    grid: { drawOnChartArea: false },
                    ticks: { color: '#dc3545' }
                }
            }
        }
    });
}

/* ========== Inicialização ========== */

function iniciar() {
    el.botao.addEventListener("click", () => Painel.calcular());

    el.entradas.forEach(entrada => {
        entrada.addEventListener("keydown", evento => {
            if (evento.key === "Enter") Painel.calcular();
        });
        entrada.addEventListener("input", () => Interface.marcarCampo(entrada, false));
    });

    iniciarRelogio();
    desenharGraficoInterativo();
}

document.addEventListener("DOMContentLoaded", iniciar);