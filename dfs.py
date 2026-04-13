"""
Algoritmo implementado (conforme slides):
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
