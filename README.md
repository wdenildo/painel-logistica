# 🏭 Dashboard de Gestão de Turno Logístico (FMCG)

Este projeto é um protótipo de painel de controle operacional desenvolvido em **Python (Streamlit)** para monitoramento e gestão de indicadores de expedição e chão de fábrica no setor de Bens de Consumo de Giro Rápido (FMCG).

O objetivo deste dashboard é transformar dados brutos de sistemas WMS/ERP em inteligência visual instantânea, permitindo que a supervisão atue proativamente em gargalos operacionais antes que eles afetem o nível de serviço ao cliente.

## 🎯 Principais Funcionalidades e KPIs

O painel foi estruturado com base na rotina real de um turno logístico de alta performance, incluindo:

*   **Visão Executiva (Causa e Efeito):** Monitoramento simultâneo do Nível de Serviço (OTIF), Volume Expedido, Pedidos Pendentes e impacto do Absenteísmo da equipe.
*   **Gestão de Pátio (Yard Management):** Visualização em tempo real do status de carregamento das docas, identificando rapidamente transportadoras em atraso para liberação de fluxo.
*   **Gestão Visual de Risco (Curva A):** Acompanhamento crítico do nível de estoque físico dos produtos de maior faturamento/giro para prevenção de rupturas durante o turno.
*   **Alertas de Auditoria:** Identificação imediata de divergências sistêmicas (erros de inventário) para atuação da equipe corretiva.

## 💻 Stack Tecnológico

*   **Python:** Linguagem base para processamento de dados e lógica de negócio.
*   **Streamlit:** Framework para criação rápida de aplicações web interativas voltadas para dados.
*   **Pandas:** Manipulação, tratamento e agregação dos dataframes de indicadores operacionais.
*   **Plotly:** Criação de visualizações gráficas dinâmicas e responsivas.

## 🧠 Sobre o Projeto e Visão Analítica

Este desenvolvimento reflete a aplicação prática da Ciência de Dados na resolução de gargalos operacionais diários. A arquitetura do código e a escolha dos indicadores foram desenhadas unindo o background em gestão logística e administração com o poder analítico do desenvolvimento em Python. O foco principal não é apenas apresentar números, mas fornecer ferramentas ágeis para a tomada de decisão em tempo real na operação.

---
*Nota: Os dados apresentados neste painel são mock data (dados simulados) gerados automaticamente para fins de demonstração da interface e lógica de negócio.*
