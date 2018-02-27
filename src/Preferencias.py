import os

from MapaUtils import carregar

preferencias = dict()


def init():
    global preferencias
    preferencias = carregar(os.path.join('builder', 'preferences.txt'))


def set(preferencia, valor):
    preferencias[preferencia] = valor


def get(preferencia):
    return preferencias.get(preferencia)


def get_int(preferencia):
    return int(get(preferencia))


def get_float(preferencia):
    return float(get(preferencia))


def get_mapa():
    return preferencias
