#!/bin/bash
# Script de compilación de la Memoria del TFG en LaTeX (Plantilla UAM / EPS)
# Genera el documento PDF completo con índices, bibliografía y referencias cruzadas.

set -e

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$DIR"

echo "=============================================="
echo "  Compilando Memoria TFG (LaTeX / BibTeX)...  "
echo "=============================================="

# 1. Primera pasada de pdflatex para registrar etiquetas y citas
echo "[1/4] Ejecutando pdflatex (1ª pasada)..."
pdflatex -interaction=nonstopmode main.tex > /dev/null 2>&1 || true

# 2. Generación de bibliografía con BibTeX
echo "[2/4] Procesando bibliografía con BibTeX..."
bibtex main > /dev/null 2>&1 || true

# 3. Segunda pasada para resolver referencias
echo "[3/4] Resolviendo referencias cruzadas (2ª pasada)..."
pdflatex -interaction=nonstopmode main.tex > /dev/null 2>&1 || true

# 4. Tercera pasada final para consolidar índices y numeración
echo "[4/4] Generando documento final (3ª pasada)..."
pdflatex -interaction=nonstopmode main.tex > /dev/null 2>&1 || true

# 5. Limpieza automática de ficheros auxiliares temporales
echo "[+] Limpiando ficheros auxiliares temporales..."
rm -f main.aux main.bbl main.blg main.log main.out main.toc main.lof main.lot main.loa main.loe main.lol main.ltb main.mw main.glo main.idx main.ist main.acn main.xdy

echo "=============================================="
echo "✅ Memoria compilada con éxito:"
echo "   $DIR/main.pdf"
echo "   Páginas: $(pdfinfo main.pdf 2>/dev/null | grep Pages | awk '{print $2}' || echo 'OK')"
echo "=============================================="
