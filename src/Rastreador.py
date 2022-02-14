#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Br.ino Qt Rastreador

Codigo da janela principal da IDE Br.ino
em PyQt5 (python 3.6)

    Icones made by Dave Gandy
    Site: https://www.flaticon.com/authors/dave-gandy
    is licensed by: http://creativecommons.org/licenses/by/3.0/"

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
author: Victor Rodrigues Pacheco
email: victor.pacheco@brino.cc
"""

import logging
import uuid
from google_measurement_protocol import event, report


log = 'registro'
ABERTURA = event('IDE', 'abriu_ide')
FECHAMENTO = event('IDE', 'fechou_ide')


def rastrear(evento):
    try:
        pass
        # TODO Salvar o id do cliente em um lugar viavel
        # report('UA-89373473-3', Preferencias.get("id_cliente"), evento)
    except:
        pass

def gerar_id_cliente():
    """
    Verifica se no arquivo de preferências há um id único para o cliente. Caso contrário, gera um.
    :return:
        None
    """
    # Comente essas linhas para teste, descomente para produção
    # TODO Arrumar onde o id eh salvo
    # if Preferencias.get("id_cliente") == "5ecd82bd-bea5-461e-b153-023626168f8e":
    #     log_info("Não há ID registrado, primeiro uso")
    #     idc = uuid.uuid4()
    #     Preferencias.set("id_cliente", str(idc))
    #     log_info("id definido como:", Preferencias.get("id_cliente"))

def log_info(m):
    log.info(m)


def log_error(m):
    log.error(m)


def log_debug(m):
    log.debug(m)


def inicializar_log():
    global log
    log = logging.getLogger("LogBrino")
    log.setLevel(logging.DEBUG)
    log_completo = logging.FileHandler('recursos/completo.log')
    log_completo.setLevel(logging.DEBUG)
    formatador = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    log_completo.setFormatter(formatador)
    log.addHandler(log_completo)
    return log