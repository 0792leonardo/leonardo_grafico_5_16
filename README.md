# Gráfico 5.16 — MP2,5

Gráfico interativo em Python + Plotly baseado no CSV fornecido e reproduzindo a estrutura da imagem de referência.

## Dados

Arquivo: `Dd_grafico_5_16.csv`

Campo das estações:

```text
estacao
```

Período exibido: **2016–2025**.

Todas as 19 estações presentes no CSV são utilizadas no gráfico. Valores ausentes são mantidos como lacunas, sem conexão artificial entre os pontos.

## Configuração

- Eixo Y: 0–30 µg/m³.
- Intervalo: 5 µg/m³.
- Linhas e marcadores por estação.
- Fundo `#DDE9F4`.
- Grade horizontal tracejada.
- Legenda horizontal.
- Tooltip interativo.
- Zoom.
- HTML autocontido.

## Arquivos

- `index.html`
- `Dd_grafico_5_16.csv`
- `gerar_grafico.py`
- `.github/workflows/pages.yml`
- `.nojekyll`
- `publicar_github.bat`
- `README.md`

## Instalação

```bash
pip install pandas plotly
```

## Gerar

```bash
python gerar_grafico.py
```

## Publicar

```bash
git init
git add .
git commit -m "Adicionar grafico 5.16 MP2.5"
git branch -M main
git remote add origin https://github.com/SEU_USUARIO/SEU_REPOSITORIO.git
git push -u origin main
```

No GitHub:

**Settings → Pages → Build and deployment → Source → GitHub Actions**

URL:

```text
https://SEU_USUARIO.github.io/SEU_REPOSITORIO/
```
