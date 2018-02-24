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
    data = json.load(open(os.path.join('recursos', 'pt-br.json')))
    palavras = list()

    for palavra_chave in data['Keywords']:
        if palavra_chave['highlight-type'] == tipo:
            string_unicode = palavra_chave['highlight']
            palavras.append(string_unicode.encode('utf-8'))

    return palavras


def traduzir(caminho):
    data = json.load(open(os.path.join('recursos', 'pt-br.json')))
    if not caminho.__contains__(".brpp") and caminho.__contains__(".ino"):
        return
    with open(caminho.replace(".brpp", ".ino"), 'w') as novo_arquivo:
        with open(os.path.join(caminho)) as arquivo_antigo:
            for linha in arquivo_antigo:
                linha_sem_espaco = linha.lstrip()
                if not linha_sem_espaco.startswith("//"):
                    for palavra_chave in data['Keywords']:
                        linha = re.sub(palavra_chave['translate'], palavra_chave['arduino'], linha)
                novo_arquivo.write(linha)
