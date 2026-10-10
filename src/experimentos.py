"""Experimentos de detecção one-class (issues #15–#18).

Separado de detection.py (modelos) e evaluation.py (métricas): aqui fica só a
orquestração — que features, que detectores, que conjuntos de teste.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from src.data import FS_HZ, montar_janelas, split_por_carga
from src.detection import DETECTORES, treinar_detector
from src.evaluation import alarmes_por_registro, erros_deteccao, metricas_deteccao
from src.features import CONJUNTOS_FEATURES, matriz_features


def dados_deteccao():
    """Janelas e features dos conjuntos principal e de generalização."""
    X, meta = montar_janelas("principal")
    F = matriz_features(X, meta["rpm"].to_numpy(), FS_HZ)
    Xg, meta_g = montar_janelas("generalizacao")
    Fg = matriz_features(Xg, meta_g["rpm"].to_numpy(), FS_HZ)
    return F, meta, Fg, meta_g


def rodar_deteccao(F, meta, Fg, meta_g, conjuntos=None, detectores=DETECTORES):
    """Treina cada detector com os normais de 0/1/2 HP e avalia em 3 HP.

    Devolve (metricas, por_registro, erros, escores_teste):
    - metricas: AUC/TPR/FPR no teste e TPR no conjunto de generalização
      (pista externa a 3 h e 12 h, todas as cargas, nunca vista no treino);
    - por_registro: taxa de alarme por gravação de teste;
    - erros: janelas de teste erradas, por experimento;
    - escores_teste: escores de cada experimento, para as curvas ROC.
    """
    conjuntos = conjuntos or list(CONJUNTOS_FEATURES)
    treino, teste = split_por_carga(meta)
    normal_treino = treino & (meta["classe"] == "normal").to_numpy()
    meta_te = meta[teste].reset_index(drop=True)
    eh_falha_te = (meta_te["classe"] != "normal").to_numpy()

    linhas, registros, erros, escores = [], [], [], {}
    for conj in conjuntos:
        cols = CONJUNTOS_FEATURES[conj]
        for nome in detectores:
            det = treinar_detector(nome, F[normal_treino], meta.loc[normal_treino, "classe"], cols)
            s = det.escore(F[teste])
            a = s > det.limiar
            ag = det.alarme(Fg)
            m = metricas_deteccao(eh_falha_te, s, a)
            linhas.append(
                {
                    "features": conj,
                    "detector": nome,
                    **m,
                    "tpr_generalizacao": ag.mean(),
                    "limiar": det.limiar,
                }
            )
            pr = alarmes_por_registro(meta_te, a).assign(features=conj, detector=nome)
            registros.append(pr)
            erros.append(erros_deteccao(meta_te, s, a, det.limiar).assign(features=conj, detector=nome))
            escores[(conj, nome)] = s
    return (
        pd.DataFrame(linhas),
        pd.concat(registros, ignore_index=True),
        pd.concat(erros, ignore_index=True),
        (eh_falha_te, escores),
    )


def tpr_por_grupo_smith(por_registro: pd.DataFrame) -> pd.DataFrame:
    """TPR por categoria de diagnosticabilidade de Smith & Randall (Y/P/N).

    Média das taxas de alarme das gravações de falha de cada grupo (cada
    gravação pesa igual, já que as janelas de uma gravação são correlacionadas).
    """
    f = por_registro[por_registro["classe"] != "normal"]
    return (
        f.groupby(["features", "detector", "grupo"])["taxa_alarme"]
        .mean()
        .unstack("grupo")
        .reindex(columns=["Y", "P", "N"])
    )


# =============================================================================
# Classificação (issues #19, #20, #22)
# =============================================================================


def rodar_classificacao(F, meta, Fg, meta_g, conjuntos=None, classificadores=None):
    """Treina em 0/1/2 HP e avalia em 3 HP; aplica também ao conjunto de
    generalização (pista externa a 3 h e 12 h, nunca vista no treino).

    Devolve um dicionário com:
    - metricas: acurácia global, por classe e taxa de "OR" na generalização;
    - matrizes: {(conjunto, classificador): matriz de confusão completa};
    - por_registro: classe predita majoritária e fração de acerto por gravação;
    - severidade: acurácia por classe e diâmetro do defeito (eixo secundário);
    - generalizacao: predições por posição, diâmetro e carga;
    - erros: janelas classificadas errado;
    - importancias: importância das features no Random Forest.
    """
    from src.classification import (
        CLASSIFICADORES,
        acuracia_por_classe,
        erros_classificacao,
        matriz_confusao,
        novo_classificador,
    )
    from src.evaluation import ler_auditoria

    conjuntos = conjuntos or list(CONJUNTOS_FEATURES)
    classificadores = classificadores or CLASSIFICADORES
    treino, teste = split_por_carga(meta)
    meta_te = meta[teste].reset_index(drop=True)
    aud = ler_auditoria()[["registro", "grupo"]]

    metricas, matrizes, por_reg, sev, gen, erros, imp = [], {}, [], [], [], [], []
    for conj in conjuntos:
        cols = CONJUNTOS_FEATURES[conj]
        for nome in classificadores:
            clf = novo_classificador(nome).fit(F.loc[treino, cols], meta.loc[treino, "classe"])
            p = clf.predict(F.loc[teste, cols])
            pg = clf.predict(Fg[cols])
            y = meta_te["classe"].to_numpy()
            tag = {"features": conj, "classificador": nome}

            acc = acuracia_por_classe(y, p)
            metricas.append(
                {**tag, "acuracia": (p == y).mean(), **{f"acc_{c}": v for c, v in acc.items()},
                 "generalizacao_OR": (pg == "OR").mean()}
            )
            matrizes[(conj, nome)] = matriz_confusao(y, p)

            d = meta_te.assign(predita=p, acerto=p == y)
            r = (
                d.groupby(["registro", "classe", "diametro_pol", "carga_hp"], dropna=False)
                .agg(acerto=("acerto", "mean"), predita_majoritaria=("predita", lambda s: s.mode().iat[0]))
                .reset_index()
                .merge(aud, on="registro", how="left")
            )
            por_reg.append(r.assign(**tag))

            s = (
                d[d["classe"] != "normal"]
                .groupby(["classe", "diametro_pol"])["acerto"].mean()
                .reset_index()
            )
            sev.append(s.assign(**tag))

            g = meta_g.assign(predita=pg)
            gen.append(
                g.groupby(["posicao_or_h", "diametro_pol", "carga_hp", "predita"])
                .size().rename("janelas").reset_index().assign(**tag)
            )
            erros.append(erros_classificacao(meta_te, p).assign(**tag))
            if nome == "random_forest":
                imp.append(pd.DataFrame({"feature": cols, "importancia": clf.feature_importances_}).assign(**tag))

    return {
        "metricas": pd.DataFrame(metricas),
        "matrizes": matrizes,
        "por_registro": pd.concat(por_reg, ignore_index=True),
        "severidade": pd.concat(sev, ignore_index=True),
        "generalizacao": pd.concat(gen, ignore_index=True),
        "erros": pd.concat(erros, ignore_index=True),
        "importancias": pd.concat(imp, ignore_index=True),
    }
