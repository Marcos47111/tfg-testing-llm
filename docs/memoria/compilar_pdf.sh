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
pdflatex -interaction=nonstopmode -halt-on-error main.tex > pdflatex_pass1.log 2>&1 || {
    echo "[-] Error en la 1ª pasada de pdflatex. Consulta docs/memoria/pdflatex_pass1.log"
    tail -n 25 pdflatex_pass1.log
    exit 1
}

# 2. Generación de bibliografía con BibTeX
echo "[2/4] Procesando bibliografía con BibTeX..."
bibtex main > bibtex.log 2>&1 || {
    echo "[-] Error al procesar BibTeX. Consulta docs/memoria/bibtex.log"
    tail -n 25 bibtex.log
    exit 1
}

# 3. Segunda pasada para resolver referencias
echo "[3/4] Resolviendo referencias cruzadas (2ª pasada)..."
pdflatex -interaction=nonstopmode -halt-on-error main.tex > pdflatex_pass2.log 2>&1 || {
    echo "[-] Error en la 2ª pasada de pdflatex. Consulta docs/memoria/pdflatex_pass2.log"
    tail -n 25 pdflatex_pass2.log
    exit 1
}

# 4. Tercera pasada final para consolidar índices y numeración
echo "[4/4] Generando documento final (3ª pasada)..."
pdflatex -interaction=nonstopmode -halt-on-error main.tex > pdflatex_pass3.log 2>&1 || {
    echo "[-] Error en la 3ª pasada de pdflatex. Consulta docs/memoria/pdflatex_pass3.log"
    tail -n 25 pdflatex_pass3.log
    exit 1
}

# 5. Verificación estricta de advertencias críticas (referencias o citas indefinidas)
echo "[+] Verificando ausencia de referencias y citas indefinidas..."
if grep -E "LaTeX Warning: Reference .* undefined|LaTeX Warning: Citation .* undefined|LaTeX Warning: There were undefined references" pdflatex_pass3.log; then
    echo "[-] ERROR CRÍTICO: Se detectaron referencias o citas indefinidas en el documento LaTeX."
    exit 1
fi

# 6. Limpieza automática de ficheros auxiliares temporales
echo "[+] Limpiando ficheros auxiliares temporales..."
rm -f main.aux main.bbl main.blg main.log main.out main.toc main.lof main.lot main.loa main.loe main.lol main.ltb main.mw main.glo main.idx main.ist main.acn main.xdy pdflatex_pass1.log bibtex.log pdflatex_pass2.log pdflatex_pass3.log

echo "=============================================="
echo "[+] Memoria compilada con éxito:"
echo "   $DIR/main.pdf"
echo "   Páginas: $(pdfinfo main.pdf 2>/dev/null | grep Pages | awk '{print $2}' || echo 'OK')"
echo "=============================================="
