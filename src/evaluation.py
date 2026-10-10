"""Métricas, matrizes de confusão e persistência dos erros para a discussão crítica.

Responsabilidades previstas:
- métricas de detecção (ROC, TPR, FPR) e de classificação (acurácia por classe);
- matriz de confusão completa, com todas as classes;
- geração da tabela de resultados exigida pelo enunciado (item 6.2);
- guarda dos casos classificados errado desde o primeiro experimento — são eles
  que sustentam os 2 pontos de discussão crítica (CLAUDE.md, seção 3, item 8).
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from src.data import FS_HZ, RAIZ, carregar_sinal, ler_manifesto
from src.features import escores_envelope, espectro_envelope, preprocessar_envelope

AUDITORIA = RAIZ / "data" / "auditoria_smith2015.csv"

# Família de frequência que cada classe deve fazer dominar no envelope.
FAMILIA_ESPERADA = {"IR": "bpfi", "OR": "bpfo", "B": "bsf"}
FAMILIAS = ("bpfo", "bpfi", "bsf")


# =============================================================================
# Validação física pelo espectro de envelope (issue #13)
# =============================================================================


def ler_auditoria() -> pd.DataFrame:
    """Diagnóstico do DE por Smith & Randall (2015, Tab. B2), por registro."""
    return pd.read_csv(AUDITORIA, comment="#", dtype=str).assign(
        registro=lambda d: d["registro"].astype(int)
    )


def validacao_fisica(
    registros: pd.DataFrame | None = None, preprocessamento: str = "bruto"
) -> pd.DataFrame:
    """Escores de envelope de cada gravação inteira e o veredito físico.

    Para cada registro, o SES do sinal completo (~10 s, resolução ~0,1 Hz) dá
    um escore por família (BPFO, BPFI, BSF; ver `escores_envelope`). A família
    `dominante` é a de maior escore. Uma falha é `confirmada` quando:
      1. a família dominante é a esperada para a classe declarada; e
      2. o escore dessa família supera o maior escore que a mesma família
         atinge nas gravações normais, que são o nível de "ruído" do método.
    O resultado é cruzado com o diagnóstico de Smith & Randall pelo método
    equivalente (M1, envelope do sinal bruto) e pelo melhor dos três métodos.

    `preprocessamento` (ver `preprocessar_envelope`): "bruto" (M1),
    "prebranqueado" (M2) ou "kurtograma". O limiar de cada família vem das
    gravações normais com o MESMO pré-processamento.
    """
    m = ler_manifesto() if registros is None else registros
    linhas = []
    for _, reg in m.iterrows():
        x = preprocessar_envelope(carregar_sinal(reg), FS_HZ, preprocessamento)
        f, ses = espectro_envelope(x, FS_HZ)
        esc = escores_envelope(f, ses, reg["rpm"]).iloc[0]
        linhas.append(
            {
                "registro": reg["id"],
                "classe": reg["classe"],
                "diametro_pol": reg["diametro_pol"],
                "posicao_or_h": reg["posicao_or_h"],
                "carga_hp": reg["carga_hp"],
                **{f"env_{k}": esc[f"env_{k}"] for k in FAMILIAS},
            }
        )
    v = pd.DataFrame(linhas)
    cols = [f"env_{k}" for k in FAMILIAS]
    v["dominante"] = v[cols].idxmax(axis=1).str.removeprefix("env_")

    normais = v[v["classe"] == "normal"]
    if normais.empty:
        raise ValueError("a validação precisa das gravações normais como referência")
    limiar = {k: normais[f"env_{k}"].max() for k in FAMILIAS}

    def veredito(r):
        esperada = FAMILIA_ESPERADA.get(r["classe"])
        if esperada is None:
            return np.nan
        return bool(r["dominante"] == esperada and r[f"env_{esperada}"] > limiar[esperada])

    v["confirmada"] = v.apply(veredito, axis=1)
    aud = ler_auditoria()[["registro", "m1", "m2", "m3", "melhor", "grupo"]]
    return v.merge(aud, on="registro", how="left").assign(preprocessamento=preprocessamento)


def resumo_validacao(v: pd.DataFrame) -> pd.DataFrame:
    """Confirmadas por classe/posição, lado a lado com Smith & Randall.

    `smith_m1_Y`: gravações que o artigo diagnostica (Y1/Y2) com o envelope do
    sinal bruto, o método equivalente ao nosso. `smith_melhor_Y`: com o melhor
    dos três métodos.
    """
    f = v[v["classe"] != "normal"].copy()
    f["grupo_classe"] = np.where(
        f["classe"] == "OR", "OR @" + f["posicao_or_h"].astype(str), f["classe"]
    )
    f["smith_m1_Y"] = f["m1"].str.startswith("Y")
    f["smith_melhor_Y"] = f["grupo"] == "Y"
    f["confirmada"] = f["confirmada"].astype(bool)
    f["concorda_m1"] = f["confirmada"] == f["smith_m1_Y"]
    ordem = ["IR", "B", "OR @6", "OR @3", "OR @12"]
    r = f.groupby("grupo_classe").agg(
        gravacoes=("registro", "size"),
        confirmadas=("confirmada", "sum"),
        smith_m1_Y=("smith_m1_Y", "sum"),
        smith_melhor_Y=("smith_melhor_Y", "sum"),
        concorda_com_m1=("concorda_m1", "sum"),
    )
    return r.loc[[o for o in ordem if o in r.index]]


# =============================================================================
# Métricas de detecção (issue #17) e registro de erros (issue #18)
# =============================================================================


def metricas_deteccao(eh_falha, escore, alarme) -> dict:
    """AUC da curva ROC e, no limiar de alarme, TPR, FPR, precisão e F1.

    `eh_falha`: verdadeiro para janelas de falha (positivas).
    - TPR (recall) = fração das falhas com alarme;
    - FPR = fração das normais com alarme;
    - precisão = fração dos alarmes que são falhas;
    - prevalência = fração de falhas no conjunto. A precisão só tem sentido
      comparada a ela: um detector que alarma sempre tem precisão igual à
      prevalência e recall 1.
    """
    from sklearn.metrics import roc_auc_score

    eh_falha = np.asarray(eh_falha, dtype=bool)
    alarme = np.asarray(alarme, dtype=bool)
    tem_as_duas = eh_falha.any() and (~eh_falha).any()
    tp = int((alarme & eh_falha).sum())
    precisao = tp / alarme.sum() if alarme.any() else np.nan
    tpr = alarme[eh_falha].mean() if eh_falha.any() else np.nan
    return {
        "auc": roc_auc_score(eh_falha, escore) if tem_as_duas else np.nan,
        "tpr": tpr,
        "fpr": alarme[~eh_falha].mean() if (~eh_falha).any() else np.nan,
        "precisao": precisao,
        "f1": 2 * precisao * tpr / (precisao + tpr) if (precisao + tpr) > 0 else np.nan,
        "prevalencia": eh_falha.mean(),
        "n_falha": int(eh_falha.sum()),
        "n_normal": int((~eh_falha).sum()),
    }


def erros_deteccao(meta: pd.DataFrame, escore, alarme, limiar: float) -> pd.DataFrame:
    """Janelas em que o detector errou: falha sem alarme (FN) ou normal com
    alarme (FP), com carga, classe, severidade e escore (CLAUDE.md, regra 8)."""
    eh_falha = (meta["classe"] != "normal").to_numpy()
    alarme = np.asarray(alarme, dtype=bool)
    errou = eh_falha != alarme
    e = meta.loc[errou, ["registro", "janela", "classe", "diametro_pol", "posicao_or_h", "carga_hp"]].copy()
    e["predito"] = np.where(alarme[errou], "anomalia", "normal")
    e["tipo_erro"] = np.where(eh_falha[errou], "FN", "FP")
    e["escore"] = np.asarray(escore)[errou]
    e["limiar"] = limiar
    return e


def alarmes_por_registro(meta: pd.DataFrame, alarme) -> pd.DataFrame:
    """Fração de janelas com alarme por gravação, com a auditoria de Smith &
    Randall (grupo Y/P/N) para estratificar as métricas."""
    d = meta[["registro", "classe", "diametro_pol", "posicao_or_h", "carga_hp"]].copy()
    d["alarme"] = np.asarray(alarme, dtype=bool)
    r = (
        d.groupby(["registro", "classe", "diametro_pol", "posicao_or_h", "carga_hp"], dropna=False)
        .agg(janelas=("alarme", "size"), taxa_alarme=("alarme", "mean"))
        .reset_index()
    )
    aud = ler_auditoria()[["registro", "m1", "grupo"]]
    return r.merge(aud, on="registro", how="left")


def comparar_preprocessamentos(registros: pd.DataFrame | None = None) -> pd.DataFrame:
    """Gravações de falha confirmadas por classe com cada pré-processamento,
    lado a lado com o que Smith & Randall diagnosticam (Y) por M1, M2 e M3.

    M2 e M3 só foram aplicados pelo artigo quando M1 ficou em P1 ou abaixo;
    quando estão vazios, o diagnóstico de M1 (Y) é contado também para eles.
    """
    vs = {p: validacao_fisica(registros, p) for p in ("bruto", "prebranqueado", "kurtograma")}
    base = vs["bruto"]
    f = base[base["classe"] != "normal"].copy()
    f["grupo_classe"] = np.where(
        f["classe"] == "OR", "OR @" + f["posicao_or_h"].astype(str), f["classe"]
    )
    linhas = {}
    for p, v in vs.items():
        f[p] = v.loc[f.index, "confirmada"].astype(bool).to_numpy()
    for k in ("m1", "m2", "m3"):
        f[f"smith_{k}"] = f[k].fillna(f["m1"]).str.startswith("Y")
    cols = ["bruto", "prebranqueado", "kurtograma", "smith_m1", "smith_m2", "smith_m3"]
    r = f.groupby("grupo_classe")[cols].sum()
    r.insert(0, "gravacoes", f.groupby("grupo_classe").size())
    ordem = ["IR", "B", "OR @6", "OR @3", "OR @12"]
    return r.loc[[o for o in ordem if o in r.index]]
