#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Br.ino Qt GerenciadorDeKeywords

Gerenciador das palavras chave da IDE Br.ino
em PyQt5 (python 2.7)

    IDE do Br.ino  Copyright (C) 2018  Br.ino

    Este arquivo e parte da IDE do Br.ino.

    A IDE do Br.ino e um software livre: voce pode redistribui-lo
    e / ou modifica-lo de acordo com os termos da Licenca Publica
    Geral GNU, conforme publicado pela Free Software Foundation,
    seja a versao 3 da Licenca , ou (na sua opcao) qualquer
    versao posterior.

    A IDE do Br.ino e distribuida na esperanca de que seja util,
    mas SEM QUALQUER GARANTIA; sem a garantia implicita de
    COMERCIALIZACAO ou ADEQUACAO A UM DETERMINADO PROPOSITO.
    Consulte a Licenca Publica Geral GNU para obter mais detalhes.

    Voce deveria ter recebido uma copia da Licenca Publica Geral
    GNU junto com este programa. Caso contrario, veja
    <https://www.gnu.org/licenses/>

website: brino.cc
author: Mateus Berardo
email: mateus.berardo@brino.cc
contributor: Victor Rodrigues Pacheco
email: victor.pacheco@brino.cc
"""

import json
import os
import re


def get_highlights(tipo):
    """
    Busca as palavras que devem ser destacadas com hightlight tipo
    :param tipo:
        Tipo de hightlight
    :return palavras:
        Lista de palavras com hightlight tipo
    """
    data = json.load(open(os.path.join('recursos', 'pt-br.json')))
    palavras = list()

    for palavra_chave in data['Keywords']:
        if palavra_chave.get('highlight-type') == tipo:
            string_unicode = palavra_chave.get('highlight')
            if string_unicode:
                palavras.append(string_unicode)

    return palavras


def traduzir(caminho):
    """
    Traduz as palavras do brino para o arduino
    :param caminho:
        Caminho do arquivo a ser traduzido
    :return:
        None
    """
    data = json.load(open(os.path.join('recursos', 'pt-br.json')))
    if not caminho.__contains__(".brpp") and caminho.__contains__(".ino"):
        return
    with open(caminho.replace(".brpp", ".ino"), 'w') as novo_arquivo:
        with open(os.path.join(caminho)) as arquivo_antigo:
            for linha in arquivo_antigo:
                linha_sem_espaco = linha.lstrip()
                if not linha_sem_espaco.startswith("//"):
                    for palavra_chave in data['Keywords']:
                        if palavra_chave.get(
                                'translate') is not None: #linha.__contains__(palavra_chave['highlight']) and
                            linha = re.sub(palavra_chave['translate'], palavra_chave['arduino'], linha)
                novo_arquivo.write(linha)
