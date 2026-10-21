#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Gráfico 5.16 – MP2,5 – Evolução das concentrações médias anuais – Baixada Santista e Interior
================================================================================

Este script gera um gráfico interativo em HTML mostrando a evolução temporal
das concentrações médias anuais de MP₂,₅ (material particulado fino) para
diferentes estações de monitoramento.

O gráfico exibe:
- Séries temporais para cada estação (2016-2025)
- Cores e símbolos automáticos para cada localidade
- Dados carregados de um arquivo CSV
- Layout otimizado para visualização e análise

MP₂,₅ = Partículas com diâmetro aerodinâmico ≤ 2,5 µm
(mais prejudiciais à saúde que MP₁₀, pois penetram mais profundamente nos pulmões)

Autor: Leonardo Rocha
Data: 2026-09-11
Versão: 1.0.0
"""

# =============================================================================
# IMPORTAÇÃO DAS BIBLIOTECAS
# =============================================================================

from pathlib import Path  # Para manipulação de caminhos de arquivos de forma segura
import pandas as pd       # Para leitura e manipulação de dados em tabelas (DataFrames)
import plotly.graph_objects as go  # Para criação de gráficos interativos


# =============================================================================
# LEITURA DOS DADOS
# =============================================================================

# Define o caminho do arquivo CSV com os dados
# O arquivo deve estar na mesma pasta do script
CSV = Path("Dd_grafico_5_16_v3.csv")

# Lê o arquivo CSV com configurações específicas:
# - sep=None: detecta automaticamente o separador (vírgula, ponto-e-vírgula, etc.)
# - engine="python": usa o parser Python para maior flexibilidade
# - encoding="utf-8-sig": lida com arquivos UTF-8 com BOM (comum em Excel)
df = pd.read_csv(CSV, sep=None, engine="python", encoding="utf-8-sig")


# =============================================================================
# CONFIGURAÇÃO DOS PARÂMETROS
# =============================================================================

# Nome da coluna que contém os nomes das estações de monitoramento
station_col = "estacao"

# Define o período de anos a ser considerado no gráfico
# O range(2016, 2026) gera anos de 2016 a 2025 (inclusive)
years = list(range(2016, 2026))


# =============================================================================
# LIMPEZA E NORMALIZAÇÃO DOS DADOS
# =============================================================================

# --- Limpeza da coluna de estações ---
# Remove espaços não-quebráveis (\xa0) que podem vir de planilhas Excel
# e remove espaços em branco no início/fim dos nomes
df[station_col] = (
    df[station_col].astype(str)
    .str.replace("\xa0", " ", regex=False)  # Substitui \xa0 por espaço normal
    .str.strip()                             # Remove espaços nas extremidades
)

# --- Conversão das colunas de anos para numérico ---
# Cada coluna de ano pode conter valores com vírgula como separador decimal
# (padrão brasileiro: "12,5" em vez de "12.5")
for year in years:
    df[str(year)] = pd.to_numeric(
        df[str(year)].astype(str).str.replace(",", ".", regex=False),
        errors="coerce"  # Valores inválidos se tornam NaN
    )


# =============================================================================
# DEFINIÇÃO DOS ESTILOS VISUAIS
# =============================================================================

# Lista de estilos (cor + símbolo) para as estações
# 19 combinações diferentes para garantir variedade visual
# Os estilos são aplicados ciclicamente se houver mais estações
# Cores escolhidas para representar temas ambientais e serem distinguíveis
styles = [
    ("#009E3D", "square-open"),    # Verde escuro - Quadrado vazado
    ("#2D558C", "circle"),          # Azul escuro - Círculo cheio
    ("#006B22", "circle"),          # Verde floresta - Círculo cheio
    ("#00A4D6", "diamond"),         # Azul ciano - Losango
    ("#F47B20", "circle"),          # Laranja - Círculo cheio
    ("#FFA500", "circle-open"),     # Laranja claro - Círculo vazado
    ("#8B2A24", "triangle-up"),     # Marrom avermelhado - Triângulo
    ("#008C3A", "square"),          # Verde médio - Quadrado cheio
    ("#FF1493", "square-open"),     # Rosa choque - Quadrado vazado
    ("#9B59B6", "circle"),          # Roxo - Círculo cheio
    ("#5E789C", "circle"),          # Azul acinzentado - Círculo cheio
    ("#E67E22", "square-open"),     # Laranja escuro - Quadrado vazado
    ("#FF0000", "circle-open"),     # Vermelho - Círculo vazado
    ("#1E3A70", "x"),               # Azul marinho - X
    ("#006B22", "circle"),          # Verde floresta (repetido) - Círculo
    ("#E58B52", "diamond-open"),    # Salmão - Losango vazado
    ("#C06C84", "circle"),          # Rosa antigo - Círculo cheio
    ("#5DADE2", "circle"),          # Azul claro - Círculo cheio
    ("#FFA45B", "circle"),          # Pêssego - Círculo cheio
]


# =============================================================================
# CRIAÇÃO DO GRÁFICO
# =============================================================================

# Inicializa uma figura vazia
fig = go.Figure()

# Itera sobre cada linha do DataFrame usando enumerate para ter o índice
# (_, row) desempacota a tupla (índice, linha), ignorando o índice com _
for i, (_, row) in enumerate(df.iterrows()):
    # Obtém o nome da estação
    station = row[station_col]
    
    # Seleciona estilo (cor + símbolo) com base no índice
    # O operador % (módulo) garante repetição cíclica se necessário
    color, symbol = styles[i % len(styles)]
    
    # Extrai os valores de MP₂,₅ para cada ano
    y = [row[str(year)] for year in years]
    
    # Adiciona uma série (traço) ao gráfico
    fig.add_trace(go.Scatter(
        # Dados do eixo X (anos) e eixo Y (valores de MP₂,₅)
        x=years, 
        y=y,
        
        # Modo: linha conectando pontos + marcadores nos pontos
        mode="lines+markers",
        
        # Nome da estação (aparece na legenda e no hover)
        name=station,
        
        # Não conecta gaps (NaN) - útil para dados faltantes
        connectgaps=False,
        
        # Configuração da linha
        line=dict(
            color=color,          # Cor definida pela lista styles
            width=1.8             # Espessura da linha (mais fina para muitas séries)
        ),
        
        # Configuração dos marcadores
        marker=dict(
            color=color,          # Cor do marcador (mesma da linha)
            symbol=symbol,        # Símbolo definido pela lista styles
            size=8                # Tamanho do marcador em pixels
        ),
        
        # Template para o tooltip (informações ao passar o mouse)
        # Nota: MP₂,₅ usa vírgula como separador decimal (padrão brasileiro)
        hovertemplate=(
            "<b>%{fullData.name}</b><br>"  # Nome da estação em negrito
            "MP₂,₅: %{y:.0f} µg/m³<extra></extra>"  # Valor sem casas decimais
        )
    ))


# =============================================================================
# CONFIGURAÇÃO DO LAYOUT (APARÊNCIA DO GRÁFICO)
# =============================================================================

fig.update_layout(
    # Tema claro com fundo branco e linhas suaves
    template="plotly_white",
    
    # Altura da figura em pixels
    height=760,
    
    # Margens ao redor do gráfico
    # Margem inferior grande (250px) para acomodar a legenda horizontal com muitas séries
    margin=dict(l=95, r=35, t=25, b=250),
    
    # Cor de fundo do papel (área externa ao gráfico)
    paper_bgcolor="#ffffff",                  # Branco
    
    # Cor de fundo da área do gráfico
    plot_bgcolor="#ffffff",                   # Branco
    
    # Modo de hover: exibe informações de todas as séries simultaneamente
    # quando o mouse passa sobre um ano específico
    hovermode="x unified",
    
    # Configuração da fonte global
    font=dict(
        family="Arial, sans-serif",           # Fonte sans-serif
        size=14,                              # Tamanho padrão
        color="#555555"                       # Cinza escuro
    ),
    
    # Configuração do eixo X (horizontal)
    xaxis=dict(
        tickmode="linear",                    # Ticks em intervalos regulares
        dtick=1,                              # Intervalo de 1 em 1 ano
        range=[2016, 2025],                   # Limites: 2016 a 2025
        showgrid=False,                       # Sem linhas de grade verticais
        zeroline=False,                       # Sem linha no zero do eixo X
        showline=True,                        # Mostra a linha do eixo X
        linecolor="#B8B8B8",                       # Cor da linha do eixo (cinza claro)
        ticks="inside"                            # Marcadores dentro do eixo
    ),
    
    # Configuração do eixo Y (vertical)
    yaxis=dict(
        title="MP₂,₅ (µg/m³)",                # Título do eixo com subscrito
        range=[0, 30],                        # Limites fixos: 0 a 30 µg/m³
        dtick=5,                              # Intervalo de 5 em 5 µg/m³
        showgrid=True,                        # Mostra linhas de grade horizontais
        gridcolor="rgba(130,130,130,0.35)",   # Cinza com 35% opacidade
        griddash="dash",                      # Linhas tracejadas
        zeroline=False,                       # Sem linha no zero do eixo Y
        showline=True,                        # Mostra a linha do eixo Y
        linecolor="#B8B8B8",                       # Cor da linha do eixo (cinza claro)
        ticks="outside"                           # Marcadores fora do eixo
    ),
    
    # Configuração da legenda
    legend=dict(
        orientation="h",                      # Horizontal (economiza espaço)
        yanchor="top",                        # Âncora no topo da legenda
        y=-0.18,                              # Posiciona abaixo do gráfico
        xanchor="center",                     # Centralizada horizontalmente
        x=0.5,                                # Centro do eixo X (50%)
        font=dict(size=11)                    # Fonte menor para muitas séries
    )
)


# =============================================================================
# EXPORTAÇÃO DO GRÁFICO
# =============================================================================

# Salva o gráfico em um arquivo HTML (autônomo, com Plotly embutido)
fig.write_html(
    "index.html",                             # Nome do arquivo de saída
    include_plotlyjs=True,                    # Inclui a biblioteca Plotly (funciona offline)
    full_html=True,                           # Gera um documento HTML completo
    config={                                  # Configurações do gráfico
        "responsive": True,                   # Gráfico se adapta ao tamanho da tela
        "displaylogo": False,                 # Remove o logo da Plotly
        "scrollZoom": True                    # Permite zoom com scroll do mouse
    }
)


# =============================================================================
# MENSAGEM DE CONFIRMAÇÃO
# =============================================================================

print("=" * 70)
print("✅ GRÁFICO DE MP₂,₅ GERADO COM SUCESSO!")
print("=" * 70)
print(f"📊 Arquivo: index.html")
print(f"📍 Local: {Path.cwd()}")
print(f"📈 Estações: {len(df)}")
print(f"📅 Período: {min(years)} a {max(years)}")
print(f"🎨 Estilos disponíveis: {len(styles)}")
print("=" * 70)
print("🌐 Abra o arquivo no navegador para visualizar o gráfico interativo.")
print("💡 Dica: Passe o mouse sobre as linhas para ver os valores detalhados.")
print("🔍 Use o scroll para zoom e arraste para navegar.")
print("=" * 70)