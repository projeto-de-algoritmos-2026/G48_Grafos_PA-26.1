"""
Escolha de estrutura:
  - Usamos um dicionário  { nó: [vizinhos] }  (lista de adjacência).
  - Vantagens:
    - Fácil de construir a partir do dicionário de dependências.
    - Permite acesso rápido aos vizinhos de um nó.
    - Simples de implementar e entender.
  - Desvantagens:
    - Pode consumir mais memória se o grafo for muito esparso.
    - Não é tão eficiente para grafos muito densos (mas não é o caso aqui).
"""

class GrafoDirigido:
    def __init__(self) -> None:
        self._adj: dict[str, list[str]] = {}

    # Operações de construção

    def adicionar_no(self, v: str) -> None:
        if v not in self._adj:
            self._adj[v] = []

    def adicionar_aresta(self, u: str, v: str) -> None:
        self.adicionar_no(u)
        self.adicionar_no(v)
        if v not in self._adj[u]:
            self._adj[u].append(v)

    # Operações de consulta

    def nos(self) -> list[str]:
        return list(self._adj.keys())

    def vizinhos(self, v: str) -> list[str]:
        return self._adj.get(v, [])

    def arestas(self) -> list[tuple[str, str]]:
        resultado = []
        for u, vizinhos in self._adj.items():
            for v in vizinhos:
                resultado.append((u, v))
        return resultado

    def __repr__(self) -> str:
        linhas = ["GrafoDirigido {"]
        for u, vizinhos in self._adj.items():
            linhas.append(f"  {u!r} → {vizinhos}")
        linhas.append("}")
        return "\n".join(linhas)
