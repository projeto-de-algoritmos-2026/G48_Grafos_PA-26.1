# Módulo C: depende de A — fecha o ciclo!  c → a → b → c
import modulo_a as funcao_a

def funcao_c():
    return funcao_a() + "resultado de c"
