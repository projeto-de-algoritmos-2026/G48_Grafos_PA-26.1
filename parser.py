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
