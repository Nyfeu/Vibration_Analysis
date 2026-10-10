# Compila os slides da apresentação.
#   make        gera build/slides.pdf
#   make clean  apaga build/
build/slides.pdf: slides.tex
	latexmk -pdf -interaction=nonstopmode -outdir=build slides.tex

clean:
	rm -rf build

.PHONY: clean
