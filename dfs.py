from graph import GrafoDirigido


def dfs_numbering(g: GrafoDirigido) -> tuple[dict[str, int], dict[str, int]]:
    """
    Executa DFS no grafo e retorna os tempos de descoberta (pre)
    e finalização (post) de cada nó.
    """

    visitado = set()
    pre = {}
    post = {}
    tempo = [1]

    def dfs_visit(v: str) -> None:
        visitado.add(v)
        pre[v] = tempo[0]
        tempo[0] += 1

        for w in g.vizinhos(v):
            if w not in visitado:
                dfs_visit(w)

        post[v] = tempo[0]
        tempo[0] += 1

    for v in g.nos():
        if v not in visitado:
            dfs_visit(v)

    return pre, post


def detectar_ciclo(g: GrafoDirigido) -> bool:
    """
    Retorna True se o grafo dirigido possui ciclo.
    Usa DFS e detecta back edge.
    """

    visitado = set()
    post = {}
    tempo = [1]
    tem_ciclo = [False]

    def dfs_visit(v: str) -> None:
        visitado.add(v)

        for w in g.vizinhos(v):
            if w not in visitado:
                dfs_visit(w)
            elif w not in post:
                tem_ciclo[0] = True

        post[v] = tempo[0]
        tempo[0] += 1

    for v in g.nos():
        if v not in visitado:
            dfs_visit(v)

    return tem_ciclo[0]
