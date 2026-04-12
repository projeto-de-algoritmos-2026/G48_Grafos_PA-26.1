# Módulo B: depende de C
from modulo_c import funcao_c

def funcao_b():
    return funcao_c() + " via b"
