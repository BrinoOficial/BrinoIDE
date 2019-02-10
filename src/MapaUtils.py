"""
Br.ino Qt mapa utils

Interface base da IDE Br.ino
em PyQt5 (python 3.6)

    IDE do Br.ino  Copyright (C) 2018  Br.ino

    Este arquivo e parte da IDE do Br.ino.

    A IDE do Br.ino e um software livre: voce pode redistribui-lo
    e / ou modifica-lo de acordo com os termos da Licenca Publica
    Geral GNU, conforme publicado pela Free Software Foundation,
    seja a versao 3 da Licenca , ou (na sua opcao) qualquer
    versao posterior.

    A IDE do Br.ino e distribuida na esperanca de que seja util,
    mas SEM QUALQUER GARANTIA sem a garantia implicita de
    COMERCIALIZACAO ou ADEQUACAO A UM DETERMINADO PROPOSITO.
    Consulte a Licenca Publica Geral GNU para obter mais detalhes.

    Voce deveria ter recebido uma copia da Licenca Publica Geral
    GNU junto com este programa. Caso contrario, veja
    <https://www.gnu.org/licenses/>

    Codigo fonte baseado no codigo do arduino

website: brino.cc
modificado por: Mateus Berardo
email: mateus.berardo@brino.cc
modificado por: Victor Rodrigues Pacheco
email: victor.pacheco@brino.cc
"""

from tempfile import mkstemp
from shutil import move
from os import fdopen, remove


def carregar(arquivo):
    """
    Faz o parsing do arquivo de preferencias
    :param arquivo:
        caminho do arquivo de preferencias
    :return prefs:
        dicionario das preferencias
    """
    prefs = dict()
    with open(arquivo, 'r') as linhas:
        for linha in linhas.readlines():
            if len(linha) < 2 or linha.startswith('#'):
                continue
            else:
                valores = linha.split("=")
                adicionar = {valores[0].strip(): valores[1].strip()}
                prefs.update(adicionar)
    return prefs


def primeiro_nivel(dicio):
    """
    Percorre o dicionario para separar em dicionarios de acordo com o primeiro nivel
    :param dicio:
        dicionario a processar
    :return opcoes:
        dicionario de primeiro nivel
    """
    opcoes = dict()
    for chave in dicio.keys():
        if chave.__contains__('.'):
            pai, filho = chave.split('.', 1)
            if opcoes.get(pai, None) is None:
                opcoes[pai] = dict()
            opcoes[pai][filho] = dicio[chave]
    return opcoes


def dicionario_superior(dicio):
    """
    Retorna dicionario de nivel superior
    :param dicio:
        dicionario alvo
    :return:
        dicionario superior
    """
    res = dict()
    for chave in dicio.keys():
        if not chave.__contains__('.'):
            res[chave] = dicio[chave]
    return res


def sub_tree(dictio, parent, sublevels=-1):
    res = dict()
    parent += "."
    parent_len = len(parent)
    for key in dictio.keys():
        if key.startswith(parent):
            nova_chave = key[parent_len:]
            key_sub_levels = len(nova_chave.split("\\."))
            if sublevels == -1 or key_sub_levels == sublevels:
                res[nova_chave] = dictio.get(key)
    return res


def descarregar(dictio, arquivo):
    tmp, caminho = mkstemp()
    with fdopen(tmp, 'w') as novas_preferencias:
        with open(arquivo, 'r') as velhas_preferencias:
            for linha in velhas_preferencias:
                if not (len(linha) < 2 or linha.startswith('#')):
                    valores = linha.split("=")
                    if valores[1].strip() != dictio.get(valores[0].strip()):
                        linha = valores[0]
                        linha += " = "
                        linha += dictio.get(valores[0].strip())
                        linha += "\n"
                novas_preferencias.write(linha)
    remove(arquivo)
    # Move new file
    move(caminho, arquivo)