"""
Algoritmo implementado (conforme slides):
É 
  DFS(G):
    time ← 1
    para todo v em G:
      se v não visitado então DFS-Visit(G, v)


  DFS-Visit(G, v):
    marque v como visitado
    pre(v) ← time; time++
    para todo w em Adj(v):
      se w não visitado então
        insira aresta (v, w) na árvore
        DFS-Visit(G, w)
    post(v) ← time; time++


Significado de pre e post:
  pre(v)  — instante em que a DFS "entrou" em v (descobriu o nó).
  post(v) — instante em que a DFS "saiu" de v (terminou de explorar
             todos os descendentes de v na árvore DFS).


  A janela [pre(v), post(v)] contém as janelas de todos os
  descendentes de v na árvore DFS.


Detecção de back edge (ciclo):
  Durante DFS-Visit(v), ao examinar um vizinho w:
    - w não visitado           → aresta de árvore (tree edge)
    - w visitado E post(w) indefinido → w ainda está "em progresso",
      ou seja, é ANCESTRAL de v → aresta (v, w) é uma BACK EDGE → CICLO.
    - w visitado E post(w) definido   → aresta cross ou forward edge (sem ciclo).
"""


from graph import GrafoDirigido


_INDEFINIDO = -1


class ResultadoDFS:
    def __init__(self) -> None:
        self.pre:  dict[str, int] = {}   # pre[v]  — tempo de entrada
        self.post: dict[str, int] = {}   # post[v] — tempo de saída
        # Cada back edge é armazenada como (v, w): v → w onde w é ancestral de v
        self.back_edges: list[tuple[str, str]] = []
        # Para cada back edge, guardamos o ciclo completo detectado
        self.ciclos: list[list[str]] = []




def dfs(grafo: GrafoDirigido) -> ResultadoDFS:
    resultado = ResultadoDFS()


    time = [1]


    # Conjunto de vértices que já iniciaram a DFS-Visit
    visitados: set[str] = set()


    # Pilha de ancestrais do caminho atual na árvore DFS.
    # Usada para reconstituir o ciclo quando uma back edge é encontrada.
    pilha_ancestrais: list[str] = []


    def dfs_visit(v: str) -> None:
        visitados.add(v)
        resultado.post[v] = _INDEFINIDO
        resultado.pre[v] = time[0]
        time[0] += 1


        pilha_ancestrais.append(v)


        for w in grafo.vizinhos(v):
            if w not in visitados:
                dfs_visit(w)
            elif resultado.post[w] == _INDEFINIDO:
                resultado.back_edges.append((v, w))


                idx = pilha_ancestrais.index(w)
                ciclo = pilha_ancestrais[idx:] + [w]
                resultado.ciclos.append(ciclo)


        pilha_ancestrais.pop()


        resultado.post[v] = time[0]
        time[0] += 1


    for v in grafo.nos():
        if v not in visitados:
            dfs_visit(v)


    return resultado




def formatar_resultado(resultado: ResultadoDFS) -> str:
    linhas = []


    linhas.append("=== DFS Numbering (pre / post) ===")
    nos_ordenados = sorted(resultado.pre.items(), key=lambda kv: kv[1])
    largura = max((len(n) for n, _ in nos_ordenados), default=6)
    linhas.append(f"  {'Módulo':<{largura}}  pre   post")
    linhas.append(f"  {'-'*largura}  ----  ----")
    for no, pre in nos_ordenados:
        post = resultado.post[no]
        linhas.append(f"  {no:<{largura}}  {pre:<4}  {post}")


    linhas.append("")


    # Ciclos encontrados
    if resultado.back_edges:
        linhas.append(f"=== Back Edges detectadas ({len(resultado.back_edges)}) ===")
        for u, v in resultado.back_edges:
            linhas.append(f"  {u!r} -> {v!r}  (v e ancestral de u -> CICLO)")
        linhas.append("")


        linhas.append("=== Ciclos encontrados ===")
        for i, ciclo in enumerate(resultado.ciclos, 1):
            caminho = " -> ".join(ciclo)
            linhas.append(f"  Ciclo {i}: {caminho}")
    else:
        linhas.append("Nenhum ciclo detectado. O grafo é um DAG.")


    return "\n".join(linhas)



Arquivo main.py
"""
main.py — Ponto de entrada do detector de dependências circulares.


Uso:
    python main.py [pasta]


    pasta : caminho para o diretório com os arquivos .py a analisar.
            Se omitido, usa a pasta "exemplo/" do diretório atual.


Fluxo:
    1. parser.py  → lê os .py e extrai deps internas com ast
    2. graph.py   → monta o GrafoDirigido a partir das deps
    3. dfs.py     → roda DFS Numbering e detecta back edges (ciclos)
    4. main.py    → exibe o resultado formatado
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
            print(f"  {modulo}  ->  {', '.join(dependencias)}")
        else:
            print(f"  {modulo}  ->  (sem dependencias internas)")
    print()


    grafo = construir_grafo(deps)


    print("=== Grafo (lista de adjacência) ===")
    for no in sorted(grafo.nos()):
        vizinhos = grafo.vizinhos(no)
        if vizinhos:
            print(f"  {no}  ->  {', '.join(vizinhos)}")
        else:
            print(f"  {no}  ->  (nenhum)")
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




Arquivo parser.py


"""
Funcionamento:
  1. Lista todos os arquivos .py da pasta-alvo.
  2. Para cada arquivo, faz o parse do AST e coleta os nomes de módulos
     referenciados em instruções `import` e `from ... import`.
  3. Filtra apenas os módulos que existem localmente na pasta (descarta
     bibliotecas externas como os, sys, re, etc.).
  4. Retorna um dicionário  módulo → lista de dependências internas.
"""


import ast
import os


def _nome_modulo(caminho_arquivo: str) -> str:
    return os.path.splitext(os.path.basename(caminho_arquivo))[0]


def _extrair_imports_do_ast(tree: ast.Module) -> list[str]:
    importados = []


    for no in ast.walk(tree):
        if isinstance(no, ast.Import):
            for alias in no.names:
                raiz = alias.name.split(".")[0]
                importados.append(raiz)


        elif isinstance(no, ast.ImportFrom):
            if no.level > 0:
                if no.module:
                    raiz = no.module.split(".")[0]
                    importados.append(raiz)
                else:
                    for alias in no.names:
                        importados.append(alias.name.split(".")[0])
            else:
                if no.module:
                    raiz = no.module.split(".")[0]
                    importados.append(raiz)


    return importados




def extrair_dependencias(pasta: str) -> dict[str, list[str]]:
    if not os.path.isdir(pasta):
        raise ValueError(f"Pasta não encontrada: {pasta}")


    # Coleta todos os nomes de módulos locais (sem .py)
    arquivos_py = [
        f for f in os.listdir(pasta) if f.endswith(".py")
    ]
    modulos_locais = {_nome_modulo(f) for f in arquivos_py}


    deps: dict[str, list[str]] = {}


    for arquivo in sorted(arquivos_py):
        modulo = _nome_modulo(arquivo)
        caminho = os.path.join(pasta, arquivo)


        with open(caminho, encoding="utf-8") as fh:
            codigo = fh.read()


        try:
            tree = ast.parse(codigo, filename=caminho)
        except SyntaxError as e:
            print(f"[parser] Aviso — erro de sintaxe em '{arquivo}': {e}")
            deps[modulo] = []
            continue


        imports_brutos = _extrair_imports_do_ast(tree)


        # Filtra: mantém apenas os que existem localmente e não são o próprio módulo
        deps[modulo] = [
            imp for imp in imports_brutos
            if imp in modulos_locais and imp != modulo
        ]


    return deps
