import os
import ast


def extrair_imports(caminho_arquivo: str) -> list[str]:
    """
    Lê um arquivo Python e retorna os módulos importados.
    """

    with open(caminho_arquivo, "r", encoding="utf-8") as f:
        arvore = ast.parse(f.read())

    imports = []

    for node in ast.walk(arvore):

        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.append(alias.name.split(".")[0])

        elif isinstance(node, ast.ImportFrom):
            if node.module:
                imports.append(node.module.split(".")[0])

    return imports


def analisar_projeto(diretorio: str) -> dict[str, list[str]]:
    """
    Percorre um diretório e cria o dicionário de dependências entre módulos.
    """

    deps = {}

    for arquivo in os.listdir(diretorio):

        if arquivo.endswith(".py"):

            caminho = os.path.join(diretorio, arquivo)
            modulo = arquivo[:-3]

            imports = extrair_imports(caminho)

            deps[modulo] = imports

    return deps
