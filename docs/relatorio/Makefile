# Relatório técnico ABNT — ECM514
#
#   make          compila o PDF em build/relatorio.pdf
#   make watch    recompila a cada salvamento (útil ao escrever)
#   make entrega  copia o PDF final para docs/relatorio/relatorio.pdf (versionável)
#   make clean    remove os auxiliares
#   make mrproper remove tudo, inclusive o PDF gerado

MAIN    := relatorio
BUILD   := build
LATEXMK := latexmk

.PHONY: all watch entrega clean mrproper check

all: $(BUILD)/$(MAIN).pdf

$(BUILD)/$(MAIN).pdf: $(MAIN).tex referencias.bib $(wildcard secoes/*.tex)
	$(LATEXMK) -pdf $(MAIN).tex

watch:
	$(LATEXMK) -pdf -pvc $(MAIN).tex

entrega: all
	cp $(BUILD)/$(MAIN).pdf $(MAIN).pdf
	@echo "PDF pronto para versionar: docs/relatorio/$(MAIN).pdf"

# Falha se algum TODO(grupo) sobrou no texto. Rodar antes da entrega final.
check:
	@! grep -rn 'TODO(grupo)' $(MAIN).tex secoes/ referencias.bib \
		|| { echo ""; echo "ERRO: ainda há TODO(grupo) pendente."; exit 1; }
	@echo "OK: nenhum TODO(grupo) pendente."

clean:
	$(LATEXMK) -c $(MAIN).tex

mrproper:
	$(LATEXMK) -C $(MAIN).tex
	rm -rf $(BUILD) $(MAIN).pdf
