# Detector de Dependências Circulares em Python

Ferramenta de linha de comando que analisa projetos Python, constrói um grafo de dependências entre módulos e detecta ciclos usando uma busca em profundidade com registro de timestamps de descoberta e finalização.

---

## Problema

Em projetos Python com múltiplos módulos, dependências circulares é um problema silencioso:

```
modulo_a.py  →  import modulo_b
modulo_b.py  →  import modulo_c
modulo_c.py  →  import modulo_a   ← ciclo!
```

Esse tipo de ciclo causa falhas de importação em tempo de execução, dificulta testes e manutenção, e é difícil de detectar manualmente conforme o projeto cresce. 

---

## Algoritmo — DFS Numbering

A busca em profundidade com timestamps atribui dois valores a cada nó durante a travessia:

- **pre(v)** — instante em que o nó foi *descoberto* (DFS chegou nele pela primeira vez)
- **post(v)** — instante em que o nó foi *finalizado* (DFS terminou de explorar todos os seus vizinhos)

```
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
```

### Detecção de ciclos via back edges

Uma **back edge** ocorre quando, durante a DFS-Visit de `v`, encontramos um vizinho `w` que já foi visitado mas ainda **não tem post(w) definido**, isso significa que `w` é ancestral de `v` na árvore DFS, e a aresta `(v → w)` fecha um ciclo.

```
v → w é back edge  ⟺  w foi visitado  AND  post(w) ainda não definido
```

**Complexidade:** O(V + E), onde V é o número de módulos e E é o número de dependências.

---

## Estrutura do projeto

```
pydep-cycle/
├── main.py        # Orquestra a análise e exibe o resultado
├── parser.py      # Lê arquivos .py e extrai imports com o módulo ast
├── graph.py       # Grafo dirigido como lista de adjacência
├── dfs.py         # DFS Numbering com pre/post e detecção de back edges
└── exemplo/       # Projeto fictício com ciclos para teste
    ├── modulo_a.py
    ├── modulo_b.py
    ├── modulo_c.py
    └── utils.py
```

---
