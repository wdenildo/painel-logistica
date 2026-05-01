"""
========================================================================
DASHBOARD DE GESTÃO DE TURNO LOGÍSTICO
Indústria FMCG - Grupo Raymundo da Fonte
========================================================================
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np
import random
from datetime import datetime, timedelta

# ─────────────────────────────────────────────────────────────────────
# CONFIGURAÇÃO DA PÁGINA
# ─────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Gestão de Turno | Raymundo da Fonte",
    page_icon="🏭",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────────────────────────────
# ESTILOS GLOBAIS (CSS) - PALETA CORPORATIVA RAYMUNDO DA FONTE
# Cores Principais: Azul Marinho Institucional e Amarelo Brilux
# ─────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&family=Syne:wght@400;600;700;800&display=swap');

    html, body, [class*="css"] { font-family: 'Syne', sans-serif; }
    
    /* Fundo escuro Azul Marinho Corporativo */
    .stApp { background-color: #081226; color: #f8fafc; }
    
    /* Sidebar mais escura */
    [data-testid="stSidebar"] { background-color: #040914; border-right: 1px solid #1e293b; }
    
    .block-container { padding-top: 1.5rem; padding-bottom: 1rem; }

    /* ── Cartões KPI (Tons de Azul Metálico) ── */
    .kpi-card {
        background: linear-gradient(135deg, #101e3d 0%, #0c162c 100%);
        border: 1px solid #1e3a8a;
        border-radius: 8px;
        padding: 20px 24px;
        text-align: center;
        position: relative;
        overflow: hidden;
        transition: transform 0.2s;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.4);
    }
    
    /* Linha superior do card usando a cor de destaque (accent) */
    .kpi-card::before {
        content: ''; position: absolute; top: 0; left: 0; right: 0; height: 4px;
        background: var(--accent);
    }
    
    .kpi-card:hover { transform: translateY(-4px); box-shadow: 0 8px 15px rgba(0, 0, 0, 0.5); border-color: #3b82f6; }
    
    .kpi-label { font-size: 0.72rem; font-weight: 700; letter-spacing: 0.12em; text-transform: uppercase; color: #cbd5e1; margin-bottom: 8px; }
    .kpi-value { font-family: 'JetBrains Mono', monospace; font-size: 2.2rem; font-weight: 700; line-height: 1; color: var(--accent); }
    .kpi-sub { font-size: 0.78rem; color: #94a3b8; margin-top: 6px; font-family: 'JetBrains Mono', monospace; }

    /* Headers de Seção no Amarelo Institucional */
    .section-header { font-size: 0.9rem; font-weight: 800; letter-spacing: 0.15em; text-transform: uppercase; color: #FFC107; border-bottom: 2px solid #1e3a8a; padding-bottom: 8px; margin: 30px 0 20px 0; }
    
    /* Produto Card */
    .prod-card { background: #101e3d; border: 1px solid #1e3a8a; border-radius: 8px; padding: 15px; text-align: center; }
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════
# SEÇÃO 1 — GERAÇÃO DE DADOS
# ═══════════════════════════════════════════════════════════════════════
def gerar_dados_turno(turno: str, seed: int = 42) -> dict:
    random.seed(seed)
    np.random.seed(seed)

    config = {
        "Manhã":  {"otif": 96.3, "vol_exp": 512, "vol_plan": 540, "pend": 18,  "diverg": 3, "absenteismo": 2},
        "Tarde":  {"otif": 88.7, "vol_exp": 390, "vol_plan": 600, "pend": 47,  "diverg": 11, "absenteismo": 8},
        "Noite":  {"otif": 93.1, "vol_exp": 445, "vol_plan": 500, "pend": 29,  "diverg": 6, "absenteismo": 4},
    }
    cfg = config[turno]

    status_opcoes = ["Carregando", "Aguardando", "Atrasada", "Livre"]
    pesos = {"Manhã": [0.4, 0.25, 0.1, 0.25], "Tarde": [0.25, 0.3, 0.3, 0.15], "Noite": [0.35, 0.2, 0.15, 0.3]}
    docas = []
    transportadoras = ["JSL Logística", "Braspress", "Atlas Trans", "Bauer Express", "—"]
    for i in range(1, 11):
        status = random.choices(status_opcoes, weights=pesos[turno])[0]
        trans = random.choice(transportadoras[:-1]) if status != "Livre" else "—"
        inicio = datetime.now() - timedelta(hours=random.uniform(0.5, 3.5))
        docas.append({
            "Doca": f"Doca {i:02d}", "Status": status, "Transportadora": trans,
            "Início": inicio.strftime("%H:%M") if status != "Livre" else "—",
            "Tempo (h)": round((datetime.now() - inicio).seconds / 3600, 1) if status != "Livre" else 0,
        })

    produtos_curva_a = {
        "Brilux 5L": {"estoque": random.randint(80, 100), "status": "Saudável", "cor": "#10b981"}, # Verde
        "Vinagre Minhoto": {"estoque": random.randint(30, 50), "status": "Alerta Baixa", "cor": "#FFC107"}, # Amarelo
        "Amaciante Sonho": {"estoque": random.randint(10, 25), "status": "Risco Ruptura", "cor": "#ef4444"} # Vermelho
    }

    return {
        "otif": cfg["otif"], "vol_exp": cfg["vol_exp"], "vol_plan": cfg["vol_plan"],
        "pendentes": cfg["pend"], "divergencias": cfg["diverg"], "absenteismo": cfg["absenteismo"],
        "df_docas": pd.DataFrame(docas), "produtos": produtos_curva_a
    }

# ═══════════════════════════════════════════════════════════════════════
# SEÇÃO 2 — SIDEBAR / FILTROS
# ═══════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("""
    <div style="text-align:center; padding: 15px; background: linear-gradient(135deg, #1e3a8a 0%, #081226 100%); border-radius: 8px; border: 1px solid #3b82f6; margin-bottom: 20px;">
        <h2 style="margin:0; color:#FFC107; font-family:'Syne'; font-weight: 800; letter-spacing: 2px;">RAYMUNDO<br><span style="color: white;">DA FONTE</span></h2>
    </div>
    """, unsafe_allow_html=True)

    turno_sel = st.selectbox("🕐 Selecione o Turno", ["Manhã", "Tarde", "Noite"], index=0)
    horarios = {"Manhã": "06:00 – 14:00", "Tarde": "14:00 – 22:00", "Noite": "22:00 – 06:00"}
    
    st.markdown("---")
    st.markdown(f"**Horário do Turno:**<br>`{horarios[turno_sel]}`", unsafe_allow_html=True)
    st.markdown(f"**Última Atualização:**<br>`{datetime.now().strftime('%d/%m/%Y %H:%M')}`", unsafe_allow_html=True)

seeds = {"Manhã": 42, "Tarde": 77, "Noite": 13}
dados = gerar_dados_turno(turno_sel, seed=seeds[turno_sel])

# ─────────────────────────────────────────────────────────────────────
# CABEÇALHO PRINCIPAL
# ─────────────────────────────────────────────────────────────────────
st.markdown(f"""
<h1 style='font-weight:800; color:#f8fafc; margin-bottom: 0px;'>Painel de Controle Logístico</h1>
<h4 style='color:#FFC107; margin-top: 0px;'>Fábrica Paulista/PE - Operação Turno {turno_sel}</h4>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════
# SEÇÃO 3 — KPIs 
# ═══════════════════════════════════════════════════════════════════════
st.markdown('<div class="section-header">▸ Visão Geral de Indicadores</div>', unsafe_allow_html=True)

col1, col2, col3, col4, col5 = st.columns(5)

# Cores dos KPIs ajustadas para brilhar no fundo azul escuro
cor_ok = "#10b981" # Esmeralda
cor_alerta = "#FFC107" # Amarelo Dourado
cor_critico = "#ef4444" # Vermelho Vivo
cor_neutro = "#3b82f6" # Azul Claro

otif = dados["otif"]
otif_cor = cor_ok if otif >= 95 else (cor_alerta if otif >= 90 else cor_critico)
with col1:
    st.markdown(f"""<div class="kpi-card" style="--accent:{otif_cor};"><div class="kpi-label">OTIF (Nível Serviço)</div><div class="kpi-value">{otif:.1f}%</div><div class="kpi-sub">Meta: 95,0%</div></div>""", unsafe_allow_html=True)

vol_pct = dados["vol_exp"] / dados["vol_plan"] * 100
vol_cor = cor_ok if vol_pct >= 80 else cor_alerta
with col2:
    st.markdown(f"""<div class="kpi-card" style="--accent:{vol_cor};"><div class="kpi-label">Expedição (Ton)</div><div class="kpi-value">{dados['vol_exp']}</div><div class="kpi-sub">{vol_pct:.0f}% da Meta ({dados['vol_plan']}t)</div></div>""", unsafe_allow_html=True)

pend = dados["pendentes"]
with col3:
    st.markdown(f"""<div class="kpi-card" style="--accent:{cor_neutro};"><div class="kpi-label">Pedidos na Fila</div><div class="kpi-value">{pend}</div><div class="kpi-sub">Aguardando Picking</div></div>""", unsafe_allow_html=True)

diverg = dados["divergencias"]
div_cor = cor_ok if diverg == 0 else cor_critico
with col4:
    st.markdown(f"""<div class="kpi-card" style="--accent:{div_cor};"><div class="kpi-label">Erros Inventário</div><div class="kpi-value">{diverg}</div><div class="kpi-sub">Requerem Auditoria</div></div>""", unsafe_allow_html=True)

absent = dados["absenteismo"]
abs_cor = cor_ok if absent <= 3 else cor_critico
with col5:
    st.markdown(f"""<div class="kpi-card" style="--accent:{abs_cor};"><div class="kpi-label">Faltas Equipe</div><div class="kpi-value">{absent}</div><div class="kpi-sub">Colaboradores Ausentes</div></div>""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════
# SEÇÃO 4 — GESTÃO DE PÁTIO E PRODUTOS CURVA A
# ═══════════════════════════════════════════════════════════════════════
st.markdown('<div class="section-header">▸ Gestão de Pátio e Produtos Chave</div>', unsafe_allow_html=True)

col_docas, col_produtos = st.columns([2, 1])

with col_docas:
    df_docas = dados["df_docas"]
    cor_status = {"Carregando": "#3b82f6", "Aguardando": "#FFC107", "Atrasada": "#ef4444", "Livre": "#1e3a8a"}
    
    fig_docas = go.Figure()
    for _, row in df_docas.iterrows():
        fig_docas.add_trace(go.Bar(
            y=[row["Doca"]], x=[1], orientation="h", marker_color=cor_status[row["Status"]],
            text=f"{row['Status']} • {row['Transportadora']}", # Adicionado o bullet de separação
            textposition="inside",
            insidetextanchor="middle", # Garante a centralização absoluta
            textfont={"size": 12, "color": "#081226" if row["Status"] == "Aguardando" else "white", "family": "Syne", "weight": "bold"}, 
            showlegend=False
        ))

    fig_docas.update_layout(
        barmode="stack", height=350, margin=dict(t=30, b=10, l=10, r=10),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(showticklabels=False, showgrid=False, zeroline=False),
        yaxis=dict(autorange="reversed", tickfont={"color": "#cbd5e1", "size": 12}),
        title=dict(text="STATUS DAS DOCAS EM TEMPO REAL", font={"color": "#FFC107", "size": 14})
    )
    st.plotly_chart(fig_docas, use_container_width=True, config={"displayModeBar": False})

with col_produtos:
    st.markdown("<h4 style='color:#FFC107; margin-top:0; font-size: 14px;'>SAÚDE DO ESTOQUE (CURVA A)</h4>", unsafe_allow_html=True)
    
    img_urls = {
        "Brilux 5L": "https://img.freepik.com/vetores-gratis/frasco-de-plastico-amarelo-com-tampa-e-rotulo-em-branco_107791-3168.jpg?w=150",
        "Vinagre Minhoto": "https://img.freepik.com/vetores-gratis/garrafa-de-vinagre-realista_1284-18086.jpg?w=150",
        "Amaciante Sonho": "https://img.freepik.com/vetores-gratis/frasco-de-plastico-de-detergente-3d-para-produtos-quimicos-domesticos_107791-16812.jpg?w=150"
    }

    for prod, info in dados["produtos"].items():
        st.markdown(f"""
        <div class="prod-card" style="border-left: 4px solid {info['cor']}; margin-bottom: 12px; display:flex; align-items:center;">
            <div style="flex: 1;">
                <img src="{img_urls[prod]}" style="width: 50px; border-radius: 4px; border: 1px solid #1e3a8a;">
            </div>
            <div style="flex: 3; text-align: left; padding-left: 15px;">
                <div style="font-weight: 800; font-size: 1.1rem; color: #f8fafc;">{prod}</div>
                <div style="color: #cbd5e1; font-family:'JetBrains Mono'; font-size: 0.85rem; margin-top: 4px;">Nível: {info['estoque']}% | <span style="color:{info['cor']}; font-weight: bold;">{info['status']}</span></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
