"""
main.py — Ponto de entrada do detector de dependências circulares.

Uso:
python main.py [pasta]

pasta : caminho para o diretório com os arquivos .py a analisar.
Se omitido, usa a pasta "exemplo/" do diretório atual.

Fluxo:
1. parser.py → lê os .py e extrai deps internas com ast
2. graph.py → monta o GrafoDirigido a partir das deps
3. dfs.py → roda DFS Numbering e detecta back edges (ciclos)
4. main.py → exibe o resultado formatado
"""

import sys
import os

from parser import extrair_dependencias
from graph import construir_grafo
from dfs import dfs, formatar_resultado


def main() -> None:
    if len(sys.argv) > 1:
        pasta = sys.argv[1]
    else:
        # Padrão: subpasta "exemplo/" ao lado deste script
        pasta = os.path.join(os.path.dirname(__file__), "exemplo_com_2_ciclos")

    print(f"Analisando pasta: {os.path.abspath(pasta)}\n")

    deps = extrair_dependencias(pasta)

    print("=== Dependências encontradas ===")
    for modulo, dependencias in sorted(deps.items()):
        if dependencias:
            print(f" {modulo} -> {', '.join(dependencias)}")
        else:
            print(f" {modulo} -> (sem dependencias internas)")
    print()

    grafo = construir_grafo(deps)

    print("=== Grafo (lista de adjacência) ===")
    for no in sorted(grafo.nos()):
        vizinhos = grafo.vizinhos(no)
        if vizinhos:
            print(f" {no} -> {', '.join(vizinhos)}")
        else:
            print(f" {no} -> (nenhum)")
    print()

    resultado = dfs(grafo)

    print(formatar_resultado(resultado))

    if resultado.back_edges:
        print(
            f"\nResumo: {len(resultado.ciclos)} ciclo(s) detectado(s). "
            "Corrija as dependências circulares acima."
        )
        sys.exit(1)
    else:
        print("\nResumo: nenhum ciclo. O projeto está livre de dependências circulares.")
        sys.exit(0)


if __name__ == "__main__":
    main()
