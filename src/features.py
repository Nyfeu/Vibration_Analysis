"""Extração de features de tempo, frequência e envelope.

Responsabilidades previstas:
- tempo: RMS, curtose, fator de crista, assimetria, valor de pico;
- frequência: FFT e análise de envelope (transformada de Hilbert);
- físico: frequências características do rolamento (BPFO, BPFI, BSF, FTF)
  a partir da geometria do SKF 6205-2RS JEM e da rotação do eixo;
- tempo-frequência (opcional): STFT, wavelet, kurtograma / spectral kurtosis
  para escolha da banda de demodulação.

Ver CLAUDE.md, seção 4.2.
"""
