#!/usr/bin/python
# -*- coding: utf-8 -*-

# TODO Apagar arquivo

"""
Br.ino Qt uploader

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


def formatar_e_dividir(src, dictio, recursivo):
    """
    TODO
    :param src:
    :param dictio:
    :param recursivo:
    :return:
    """
    for i in range(10):

        res = substituir_do_mapa(src, dictio)
        if not recursivo:
            break
        if res == src:
            break
        src = res
    return separacao_quotes(src, '"\'', False)


def substituir_do_mapa(src, dictio, delimitador_esquerdo='{', delimitador_direito='}'):
    """
    :param src:
    :param dictio:
    :param delimitador_esquerdo:
    :param delimitador_direito:
    :return:
    """

    for key in dictio.keys():
        try:
            keyword = delimitador_esquerdo + key + delimitador_direito
        except TypeError:
            keyword = delimitador_esquerdo + str(key, 'utf-8') + delimitador_direito
        if dictio.get(key) is not None and keyword is not None:
            src = src.replace(keyword, dictio.get(key))

    return src


def separacao_quotes(src, quote_chars, arg_vazios):
    """
    TODO
    :param src:
    :param quote_chars:
    :param arg_vazios:
    :return:
    """
    res = list()
    arg_escapado = None
    char_escapador = None
    for s in src.split(" "):
        if char_escapador is None:
            first = None
            if len(s) > 0:
                first = s[0:1]
            if first is None or not quote_chars.__contains__(first):
                if not len(s.strip()) == 0 or arg_vazios:
                    res.append(s)
                continue
            char_escapador = first
            s = s[1:]
            arg_escapado = ""
        if not s.endswith(char_escapador):
            arg_escapado += s + " "
            continue
        arg_escapado += s[0:len(s) - 1]
        if not len(arg_escapado.strip()) == 0 or arg_vazios:
            res.append(arg_escapado)
            char_escapador = None
    if char_escapador is not None:
        print("Erro")
    return res
