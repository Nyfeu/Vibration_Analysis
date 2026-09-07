# Ambiente de desenvolvimento do projeto ECM514.
# Objetivo: qualquer pessoa do grupo abre o repositório e tem exatamente o mesmo
# Python e a mesma distribuição TeX, sem instalar nada na máquina.

FROM mcr.microsoft.com/devcontainers/python:3.11-bookworm

# ---- Distribuição TeX ----------------------------------------------------
# Subconjunto, não texlive-full (~5 GB). O que cada pacote traz:
#   texlive-latex-recommended/-extra  base + booktabs, multirow, float, siunitx
#   texlive-publishers                a classe abntex2
#   texlive-bibtex-extra              biblatex e biblatex-abnt
#   texlive-lang-portuguese           hifenização pt-BR (babel brazil)
#   texlive-fonts-recommended/lmodern Latin Modern
#   texlive-science                   siunitx
#   latexmk + biber                   cadeia de compilação usada pelo Makefile
# Se faltar algum pacote LaTeX no futuro, acrescente aqui — nunca via tlmgr
# dentro do container, senão o ambiente deixa de ser reprodutível.
RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        texlive-latex-recommended \
        texlive-latex-extra \
        texlive-publishers \
        texlive-bibtex-extra \
        texlive-lang-portuguese \
        texlive-fonts-recommended \
        texlive-science \
        lmodern \
        latexmk \
        biber \
        make \
        poppler-utils \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# ---- Dependências Python -------------------------------------------------
COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r /tmp/requirements.txt \
    && rm /tmp/requirements.txt
