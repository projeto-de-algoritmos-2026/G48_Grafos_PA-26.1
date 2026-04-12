# Módulo D: depende de A, mas não faz parte do ciclo em si
import sys
from utils import funcao_util
from modulo_a import funcao_a

def funcao_d():
    return funcao_a() + " via d " + funcao_util() 
