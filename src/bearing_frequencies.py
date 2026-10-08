"""Frequências características de defeito do rolamento do drive end do CWRU.

Rolamento: SKF 6205-2RS JEM (o mesmo das Tabelas 1 e 2 do relatório).

Fórmulas cinemáticas (Smith & Randall, 2015, p. 3), com f_r a rotação do eixo
em Hz, n o número de esferas, d o diâmetro da esfera, D o diâmetro primitivo
e phi o ângulo de contato:

    BPFO = (n * f_r / 2) * (1 - (d / D) * cos(phi))     pista externa
    BPFI = (n * f_r / 2) * (1 + (d / D) * cos(phi))     pista interna
    FTF  = (f_r / 2)     * (1 - (d / D) * cos(phi))     gaiola
    BSF  = (D * f_r / (2 * d)) * (1 - ((d / D) * cos(phi)) ** 2)   esfera

Atenção: as fórmulas supõem ausência de escorregamento. Na prática, desvios de
1% a 2% em relação ao valor calculado são comuns (Smith & Randall, 2015, p. 3),
por isso use `tolerance_band` ao procurar picos no espectro.
"""

from dataclasses import dataclass
from math import cos, radians


@dataclass(frozen=True)
class BearingGeometry:
    """Geometria do rolamento. Comprimentos na mesma unidade (aqui, polegadas)."""

    n_balls: int
    ball_diameter: float  # d
    pitch_diameter: float  # D
    contact_angle_deg: float = 0.0  # phi


# Fontes:
#  - d e D: CWRU Bearing Data Center, página "Bearing Specifications"
#    (drive end: ball diameter 0.3126 in, pitch diameter 1.537 in).
#  - n = 9: Smith & Randall (2015), p. 10. Essa página do CWRU não informa n.
SKF_6205_DE = BearingGeometry(n_balls=9, ball_diameter=0.3126, pitch_diameter=1.537)


@dataclass(frozen=True)
class CharacteristicFrequencies:
    """Frequências em Hz."""

    bpfo: float  # pista externa
    bpfi: float  # pista interna
    bsf: float  # esfera (ball spin frequency)
    ftf: float  # gaiola

    @property
    def bsf_2x(self) -> float:
        """2 x BSF.

        É o valor que a página do CWRU chama de "Rolling Element" (4,7135 x f_r):
        a esfera com defeito bate nas duas pistas a cada giro. Já Smith & Randall
        usam BSF (2,357 x f_r) e dizem que os harmônicos pares costumam dominar.
        Ao comparar com o espectro de envelope, decida e declare qual convenção usa.
        """
        return 2.0 * self.bsf


def characteristic_frequencies(
    rpm: float, geometry: BearingGeometry = SKF_6205_DE
) -> CharacteristicFrequencies:
    """Calcula BPFO, BPFI, BSF e FTF (em Hz) a partir da rotação em rpm.

    Prefira a rotação medida em cada arquivo .mat (variável RPM) à nominal,
    porque a rotação real cai com a carga.
    """
    if rpm <= 0:
        raise ValueError(f"rpm deve ser positivo, recebido {rpm!r}")

    f_r = rpm / 60.0
    n = geometry.n_balls
    d = geometry.ball_diameter
    big_d = geometry.pitch_diameter
    ratio = (d / big_d) * cos(radians(geometry.contact_angle_deg))

    return CharacteristicFrequencies(
        bpfo=n * f_r / 2.0 * (1.0 - ratio),
        bpfi=n * f_r / 2.0 * (1.0 + ratio),
        bsf=big_d * f_r / (2.0 * d) * (1.0 - ratio**2),
        ftf=f_r / 2.0 * (1.0 - ratio),
    )


def tolerance_band(freq_hz: float, tol: float = 0.02) -> tuple[float, float]:
    """Janela de busca em torno de uma frequência teórica (padrão: +-2%)."""
    return freq_hz * (1.0 - tol), freq_hz * (1.0 + tol)
