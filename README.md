# Detector de Dependências Circulares em Python

Número da Lista: 48<br>
Conteúdo da Disciplina: Grafos<br>

## Alunos
|Matrícula | Aluno |
| -- | -- |
| 23/1034082  |  ARTUR HANDOW KRAUSPENHAR |
| 21/1031593  |  ANDRE LOPES DE SOUSA |

**Apresentação:** https://www.youtube.com/watch?v=11ndWVb6234

## Sobre 

Ferramenta de linha de comando que analisa projetos Python, constrói um grafo de dependências entre módulos e detecta ciclos usando uma busca em profundidade com registro de timestamps de descoberta e finalização.

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
    ├── main.py
    ├── modulo_a.py
    ├── modulo_b.py
    ├── modulo_c.py
    ├── modulo_d.py
    └── utils.py
```

---

## Instalação

Linguagem: Python 3.8+<br>
Framework: Sem Framework<br>

```bash
# Analisar um projeto
python main.py /caminho/para/seu/projeto

# Testar com o exemplo incluído
python main.py ./exemplo_com_2_ciclos
```

**Saída esperada (no exemplo):**

```
Analisando pasta: E:\GitHub\Trabalho 1 PA\exemplo_com_2_ciclos

=== Dependências encontradas ===
  main -> modulo_a, modulo_d
  modulo_a -> modulo_b
  modulo_b -> modulo_c
  modulo_c -> modulo_a
  modulo_d -> utils, modulo_a
  utils -> modulo_d

=== Grafo (lista de adjacência) ===
  main -> modulo_a, modulo_d
  modulo_a -> modulo_b
  modulo_b -> modulo_c
  modulo_c -> modulo_a
  modulo_d -> utils, modulo_a
  utils -> modulo_d

=== DFS Numbering (pre / post) ===
  Módulo    pre   post
  --------  ----  ----
  main      1     12
  modulo_a  2     7
  modulo_b  3     6
  modulo_c  4     5
  modulo_d  8     11
  utils     9     10

=== Back Edges detectadas (2) ===
  'modulo_c' -> 'modulo_a'  (v e ancestral de u -> CICLO)
  'utils' -> 'modulo_d'  (v e ancestral de u -> CICLO)

=== Ciclos encontrados ===
  Ciclo 1: modulo_a -> modulo_b -> modulo_c -> modulo_a
  Ciclo 2: modulo_d -> utils -> modulo_d

Resumo: 2 ciclo(s) detectado(s). Corrija as dependências circulares acima.
```

---

## Detalhes técnicos

| Componente | Responsabilidade |
|---|---|
| `parser.py` | Usa o módulo `ast` para extrair imports sem executar o código |
| `graph.py` | Representa o grafo como dicionário de listas de adjacência |
| `dfs.py` | Implementa DFS Numbering com variável `time` global e detecção de back edges |
| `main.py` | Recebe o caminho, orquestra as etapas e formata a saída |

O parser considera apenas imports internos ao projeto, imports de bibliotecas externas (`os`, `sys`, `requests`, etc.) são ignorados automaticamente comparando os nomes encontrados com os módulos presentes na pasta analisada.
