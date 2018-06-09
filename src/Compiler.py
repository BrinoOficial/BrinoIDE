#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Br.ino Qt DestaqueSintaxe

Codigo de destaque da sintaxe do brpp e ino da IDE Br.ino
em PyQt5 (python 3.6)

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

import os
from subprocess import Popen, PIPE

import Main
import Preferencias


def compilar_arduino_builder(caminho, placa_alvo, plataforma_alvo, pacote_alvo, temp, cache):
    """
    usa o arduino builder para compilar
    :param caminho:
        Caminho do codigo a ser compilado
    :param placa_alvo:
        Placa alvo
    :param plataforma_alvo:
        Plataforma alvo
    :param pacote_alvo:
        Pacote alvo
    :param temp:
        Pasta temporaria para salvar os .hex
    :param cache:
        Pasta para fazer cache do nucleo compilado
    :return output:
        resultado do comando de compilacao
    """
    pacotes_instalados = os.path.abspath(os.path.join('.', 'builder', '.arduino15', 'packages'))
    cmd = os.path.abspath(os.path.join('.', 'builder', 'arduino-builder'))
    cmd += " -compile"
    cmd += " -logger=human"
    cmd = adicionar_hardware_se_existe(cmd, os.path.abspath(os.path.join('.', 'builder', 'hardware')))
    cmd = adicionar_hardware_se_existe(cmd, pacotes_instalados)
    cmd = adicionar_hardware_se_existe(cmd, os.path.abspath(os.path.join(caminho, 'hardware')))
    cmd = adicionar_ferramenta_se_existe(cmd, os.path.abspath(os.path.join('.', 'builder', 'tools-builder')))
    cmd = adicionar_ferramenta_se_existe(cmd, os.path.abspath(os.path.join('.', 'builder', 'hardware', 'tools', 'avr')))
    cmd = adicionar_ferramenta_se_existe(cmd, pacotes_instalados)
    cmd = adicionar_se_existe(cmd, ' -built-in-libraries ', os.path.abspath(os.path.join('.', 'builder', 'libraries')))
    cmd = adicionar_se_existe(cmd, ' -libraries ', os.path.join(Main.get_caminho_padrao(), 'bibliotecas'))
    fqbn = pacote_alvo.get_id() + ":" + plataforma_alvo.get_id() + ":" + placa_alvo.get_id() + opcoes_da_placa(
        placa_alvo)
    cmd += " -fqbn=" + fqbn
    # TODO vidpid
    cmd += " -ide-version=10805"
    cmd += " -build-path " + temp
    # TODO warning level
    cmd += " -build-cache " + cache
    # TODO mais preferencias
    cmd += " " + os.path.dirname(caminho)
    p = Popen(cmd, stdout=PIPE, stderr=PIPE, stdin=PIPE, shell=True)
    output = p.stdout.read()
    output += p.stderr.read()
    return output


def opcoes_da_placa(placa):
    """
    opcoes de placa
    :param placa:
    :return "":
        ""
    """
    opcoes = ":"
    for menu_id in placa.menu_opcoes.keys():
        opcoes += menu_id + "="
        opcoes += Preferencias.get("custom_" + menu_id)[len(placa.get_id()) + 1:]
        opcoes += ","

    return opcoes[:len(opcoes) - 1]


def adicionar_hardware_se_existe(string, arquivo):
    """
    Caso exista o parametro arquivo, adiciona ele ao comando como uma opcao de hardware
    :param string:
        comando
    :param arquivo:
        arquivo a adicionar
    :return:
        comando com acresimos
    """
    return adicionar_se_existe(string, " -hardware ", arquivo)


def adicionar_ferramenta_se_existe(string, arquivo):
    """
    Caso exista o parametro arquivo, adiciona ele ao comando como uma opcao de ferramenta
    :param string:
        comando
    :param arquivo:
        arquivo a adicionar
    :return:
        comando com acresimos
    """
    return adicionar_se_existe(string, " -tools ", arquivo)


def adicionar_se_existe(string, opcao, arquivo):
    """
    adiciona arquivo como uma opcao do tipo opcao, caso exista o aquivo, ao comando string
    :param string:
        comando
    :param opcao:
        tipo de opcao
    :param arquivo:
        arquivo a adicionar
    :return:
        comando com acresimos
    """
    if os.path.exists(arquivo):
        return string + opcao + arquivo
    return string
