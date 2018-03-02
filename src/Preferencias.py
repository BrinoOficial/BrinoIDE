import os

from MapaUtils import carregar

preferencias = dict()


def init():
    """
    Carrega o arquivo de preferencias
    :return:
        None
    """
    global preferencias
    preferencias = carregar(os.path.join('builder', 'preferences.txt'))


def set(preferencia, valor):
    """
    Adiciona novas preferencias
    :param preferencia:
        Preferencia a ser salva
    :param valor:
        Valor da preferencia
    :return:
        None
    """
    preferencias[preferencia] = valor


def get(preferencia):
    """
    TODO
    :param preferencia:
    :return:
    """
    return preferencias.get(preferencia)


def get_int(preferencia):
    """
    TODO
    :param preferencia:
    :return:
    """
    return int(get(preferencia))


def get_float(preferencia):
    """
    TODO
    :param preferencia:
    :return:
    """
    return float(get(preferencia))


def get_mapa():
    """
    TODO
    :return:
    """
    return preferencias
