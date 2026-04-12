# Módulo A: depende de B e usa uma biblioteca externa (os)
import os
from modulo_b import funcao_b

def funcao_a():
    return funcao_b() + " via a"
