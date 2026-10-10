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


def rodar_classificacao(F, meta, Fg, meta_g, conjuntos=None, modelos=("Random Forest", "SVM (RBF)")):
    """Roteiro das aulas, para cada conjunto de features:

    1. seleção de modelos: acurácia de todos os candidatos na validação cruzada
       do treino (por carga, e embaralhada só para comparação);
    2. GridSearchCV dos modelos em `modelos`, com CV por carga;
    3. o melhor pipeline de cada busca é avaliado no teste (3 HP) e aplicado
       ao conjunto de generalização (pista externa a 3 h e 12 h).

    Devolve um dicionário com metricas, selecao, melhores_parametros,
    matrizes, relatorios (classification_report), por_registro, severidade,
    generalizacao, erros e importancias (Random Forest).
    """
    from sklearn.metrics import classification_report

    from src.classification import (
        acuracia_por_classe,
        ajustar_hiperparametros,
        erros_classificacao,
        matriz_confusao,
        selecionar_modelos,
    )
    from src.evaluation import ler_auditoria

    conjuntos = conjuntos or list(CONJUNTOS_FEATURES)
    treino, teste = split_por_carga(meta)
    meta_te = meta[teste].reset_index(drop=True)
    y_tr = meta.loc[treino, "classe"]
    cargas_tr = meta.loc[treino, "carga_hp"]
    aud = ler_auditoria()[["registro", "grupo"]]

    metricas, selecao, params, matrizes, relatorios = [], [], [], {}, {}
    por_reg, sev, gen, erros, imp = [], [], [], [], []
    for conj in conjuntos:
        cols = CONJUNTOS_FEATURES[conj]
        x_tr = F.loc[treino, cols]
        selecao.append(selecionar_modelos(x_tr, y_tr, cargas_tr).assign(features=conj))
        for nome in modelos:
            busca = ajustar_hiperparametros(nome, x_tr, y_tr, cargas_tr)
            clf = busca.best_estimator_
            p = clf.predict(F.loc[teste, cols])
            pg = clf.predict(Fg[cols])
            y = meta_te["classe"].to_numpy()
            tag = {"features": conj, "classificador": nome}
            params.append({**tag, "cv_por_carga": busca.best_score_, **busca.best_params_})

            acc = acuracia_por_classe(y, p)
            metricas.append(
                {**tag, "cv_por_carga": busca.best_score_, "acuracia": (p == y).mean(),
                 **{f"acc_{c}": v for c, v in acc.items()}, "generalizacao_OR": (pg == "OR").mean()}
            )
            matrizes[(conj, nome)] = matriz_confusao(y, p)
            relatorios[(conj, nome)] = pd.DataFrame(
                classification_report(y, p, output_dict=True, zero_division=0)
            ).transpose()

            d = meta_te.assign(predita=p, acerto=p == y)
            r = (
                d.groupby(["registro", "classe", "diametro_pol", "carga_hp"], dropna=False)
                .agg(acerto=("acerto", "mean"), predita_majoritaria=("predita", lambda s: s.mode().iat[0]))
                .reset_index()
                .merge(aud, on="registro", how="left")
            )
            por_reg.append(r.assign(**tag))
            sev.append(
                d[d["classe"] != "normal"].groupby(["classe", "diametro_pol"])["acerto"].mean()
                .reset_index().assign(**tag)
            )
            gen.append(
                meta_g.assign(predita=pg)
                .groupby(["posicao_or_h", "diametro_pol", "carga_hp", "predita"])
                .size().rename("janelas").reset_index().assign(**tag)
            )
            erros.append(erros_classificacao(meta_te, p).assign(**tag))
            if nome == "Random Forest":
                imp.append(
                    pd.DataFrame({"feature": cols, "importancia": clf.named_steps["clf"].feature_importances_})
                    .assign(**tag)
                )

    return {
        "metricas": pd.DataFrame(metricas),
        "selecao": pd.concat(selecao, ignore_index=True),
        "melhores_parametros": pd.DataFrame(params),
        "matrizes": matrizes,
        "relatorios": relatorios,
        "por_registro": pd.concat(por_reg, ignore_index=True),
        "severidade": pd.concat(sev, ignore_index=True),
        "generalizacao": pd.concat(gen, ignore_index=True),
        "erros": pd.concat(erros, ignore_index=True),
        "importancias": pd.concat(imp, ignore_index=True),
    }


def rodar_cnn(meta=None, entradas=None):
    """CNN 1D sobre as janelas (issue #21), treino 0/1/2 HP e teste 3 HP.

    Exige PyTorch. Devolve (metricas, matrizes, por_registro).
    """
    from src.classification import acuracia_por_classe, matriz_confusao
    from src.cnn import ENTRADAS, ClassificadorCNN

    X, meta = montar_janelas("principal")
    Xg, _ = montar_janelas("generalizacao")
    treino, teste = split_por_carga(meta)
    meta_te = meta[teste].reset_index(drop=True)
    y = meta_te["classe"].to_numpy()
    metricas, matrizes, por_reg = [], {}, []
    for entrada in entradas or ENTRADAS:
        clf = ClassificadorCNN(entrada).fit(X[treino], meta.loc[treino, "classe"])
        p = clf.predict(X[teste])
        pg = clf.predict(Xg)
        tag = {"features": f"sinal {entrada}", "classificador": "CNN 1D"}
        acc = acuracia_por_classe(y, p)
        metricas.append(
            {**tag, "acuracia": (p == y).mean(), **{f"acc_{c}": v for c, v in acc.items()},
             "generalizacao_OR": (pg == "OR").mean()}
        )
        matrizes[(f"sinal {entrada}", "CNN 1D")] = matriz_confusao(y, p)
        d = meta_te.assign(acerto=p == y, predita=p)
        por_reg.append(
            d.groupby(["registro", "classe"]).agg(
                acerto=("acerto", "mean"), predita_majoritaria=("predita", lambda s: s.mode().iat[0])
            ).reset_index().assign(**tag)
        )
    return pd.DataFrame(metricas), matrizes, pd.concat(por_reg, ignore_index=True)


# =============================================================================
# Generalização entre montagens
# =============================================================================

# Família de envelope dominante -> classe prevista pela física (sem treino).
REGRA_FISICA = {"env_bpfo": "OR", "env_bpfi": "IR", "env_bsf": "B"}


def prever_regra_fisica(F: pd.DataFrame) -> pd.Series:
    """Classe de falha pela família de envelope de maior escore em cada janela.
    Não usa treino: não tem como memorizar montagens."""
    return F[list(REGRA_FISICA)].idxmax(axis=1).map(REGRA_FISICA)


def classificacao_por_montagem(F, meta, Fg=None, meta_g=None, conjuntos=None, modelos=None):
    """Tipo de falha (IR, B, OR) com validação deixando um diâmetro de fora.

    No CWRU, cada combinação de defeito e diâmetro foi ensaiada numa única
    montagem, presente nas quatro cargas. Deixar um diâmetro inteiro de fora
    obriga o modelo a classificar montagens que nunca viu — o teste que o split
    por carga não faz. Só as falhas entram (o normal não tem diâmetro). A regra
    física entra como referência sem treino.

    Devolve (metricas, por_diametro).
    """
    from sklearn.model_selection import LeaveOneGroupOut, cross_val_predict

    from src.classification import acuracia_por_classe, modelos_candidatos

    falhas = (meta["classe"] != "normal").to_numpy()
    y = meta.loc[falhas, "classe"].to_numpy()
    grupos = meta.loc[falhas, "diametro_pol"].to_numpy()
    conjuntos = conjuntos or list(CONJUNTOS_FEATURES)
    modelos = modelos or ["Random Forest", "SVM (RBF)", "KNN (k=9)"]
    classes = ["IR", "B", "OR"]

    def registrar(tag, p):
        acc = acuracia_por_classe(y, p, classes)
        linhas.append({**tag, "acuracia": (p == y).mean(), **{f"acc_{c}": v for c, v in acc.items()}})
        for d in np.unique(grupos):
            sel = grupos == d
            por_d.append({**tag, "diametro_fora": d, "acuracia": (p[sel] == y[sel]).mean()})

    linhas, por_d = [], []
    for conj in conjuntos:
        x = F.loc[falhas, CONJUNTOS_FEATURES[conj]]
        for nome in modelos:
            p = cross_val_predict(
                modelos_candidatos()[nome], x, y, groups=grupos, cv=LeaveOneGroupOut(), n_jobs=-1
            )
            registrar({"features": conj, "modelo": nome}, p)
    registrar({"features": "envelope", "modelo": "Regra física (sem treino)"},
              prever_regra_fisica(F.loc[falhas]).to_numpy())

    try:  # CNN 1D, se o PyTorch estiver disponível
        from src.cnn import ENTRADAS, ClassificadorCNN

        X, meta_x = montar_janelas("principal")
        Xf = X[(meta_x["classe"] != "normal").to_numpy()]
        for entrada in ENTRADAS:
            p = np.empty(len(y), dtype=object)
            for d in np.unique(grupos):
                tr, te = grupos != d, grupos == d
                clf = ClassificadorCNN(entrada)
                clf.classes_ = classes
                p[te] = clf.fit(Xf[tr], y[tr]).predict(Xf[te])
            registrar({"features": f"sinal {entrada}", "modelo": "CNN 1D"}, p)
    except ImportError:
        pass
    return pd.DataFrame(linhas), pd.DataFrame(por_d)
