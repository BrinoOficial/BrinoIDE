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

website: https://brino.cc
github: https://github.com/BrinoOficial/BrinoIDE
author: Victor Rodrigues Pacheco
author: Gabriel Rodrigues Pacheco
"""

import os
import re
from time import sleep
from subprocess import Popen, PIPE

import Rastreador
from GerenciadorDeKeywords import traduzir


def compilar_arduino_cli(caminho, plataforma_alvo, carregar: False, porta_alvo: "None"):
    """
    usa o arduino cli para compilar
    :param caminho:
        Caminho do codigo a ser compilado
    :param plataforma_alvo:
        Placa arduino para a qual o codigo deve ser compilado
    :param carregar:
        Flag que aponta se deve ser carregado o codigo
    :param porta_alvo:
        Porta serial para a qual o codigo sera carregado
    :return output:
        resultado do comando de compilacao
    """
    # Traduz o codigo
    traduzir(caminho)
    caminho_bibliotecas = get_caminho_padrao() + str("/Bibliotecas/")
    print(caminho_bibliotecas)
    caminho = caminho.replace("brpp", "ino")

    # Seleciona o Arduino CLI correto pro sistema operacional
    if os.path.isfile('arduino-cli.exe'):
        arn_cli = os.path.abspath(os.path.join('.', 'arduino-cli.exe'))
    else:
        arn_cli = os.path.abspath(os.path.join('.', 'arduino-cli'))

    if carregar:
        # Compila e carrega o codigo
        cmd = '"' + arn_cli + '"' + " compile -b" + plataforma_alvo + " " + '"' + caminho + '"' + " -p " + str(porta_alvo) + " -u" + " --library " + '"' + caminho_bibliotecas + '"'
    else:
        # Compila o codigo
        cmd = '"' + arn_cli + '"' + " compile --fqbn " + plataforma_alvo + " " + '"' + caminho + '"' + " --library " + '"' + caminho_bibliotecas + '"'
    print(cmd)
    Rastreador.log_info("Processo compilar - > CMD:")
    Rastreador.log_info(cmd)
    p = Popen(cmd, stdout=PIPE, stderr=PIPE, stdin=PIPE, shell=True)
    # TODO Criar timeout para nao travar o codigo caso de errado
    output = p.stdout.read()
    output += p.stderr.read()
    return output


def get_caminho_padrao():
    """
    Pega o caminho padrao ate a pasta de RascunhosBrino
    :return:
        Caminho padrao
    """
    caminho_padrao = os.path.expanduser("~")
    docu = re.compile("Documen.*")
    pastas = os.listdir(caminho_padrao)
    documentos = list(filter(docu.match, pastas))
    caminho_padrao = os.path.join(caminho_padrao, documentos[0], "RascunhosBrino")
    caminho_padrao = caminho_padrao.replace('\\', "/")
    return caminho_padrao


def listar_todas_placas_compativeis_cli():
    """
    Funcao para listar as placas compativeis com o arduino cli
    :return output:
        resultado do comando de listar palcas (Uma lista de strings com as placas (nome e codigo FQBN dela)
    """
    try:
        # Seleciona o Arduino CLI correto pro sistema operacional
        if os.path.isfile('arduino-cli.exe'):
            arn_cli = os.path.abspath(os.path.join('.', 'arduino-cli.exe'))
        else:
            arn_cli = os.path.abspath(os.path.join('.', 'arduino-cli'))
        cmd = '"' + arn_cli + '"' + " board listall"
        p = Popen(cmd, stdout=PIPE, stderr=PIPE, stdin=PIPE, shell=True)
        print(cmd)
        lista_de_placas = p.stdout.read()
        lista_de_placas += p.stderr.read()
        return lista_de_placas.decode()
    except Exception as e:
        Rastreador.log_error("Erro ao listar todas placas compativeis cli: ")
        Rastreador.log_error(e)
        Rastreador.log_error("Lista de placas obtidas na operação:")


def listar_todas_placas_conectadas_cli():
    """
    Funcao para listar as placas Arduino conectadas ao computador
    :return output:
        resultado do comando de listar palcas conectadas (Uma lista de strings com as placas (nome e codigo FQBN dela)
    """
    try:
        # Seleciona o Arduino CLI correto pro sistema operacional
        if os.path.isfile('arduino-cli.exe'):
            arn_cli = os.path.abspath(os.path.join('.', 'arduino-cli.exe'))
        else:
            arn_cli = os.path.abspath(os.path.join('.', 'arduino-cli'))
        cmd = '"' + arn_cli + '"' + " board list"
        p = Popen(cmd, stdout=PIPE, stderr=PIPE, stdin=PIPE, shell=True)
        lista_portas = list()
        lista_portas_lidas = p.stdout.read().decode().split('\n')
        lista_portas_lidas.pop(0)
        while '' in lista_portas_lidas:
            lista_portas_lidas.remove('')
        for porta in lista_portas_lidas:
            temp = porta.split()
            lista_portas.append(temp[0])
        return lista_portas
    except Exception as e:
        Rastreador.log_error("Erro ao listar todas placas conectadas cli: ")
        Rastreador.log_error(e)


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
        return string + opcao + '"' + arquivo + '"'
    return string


def acompanha_portas_conectadas(objeto_principal):
    """
    Verifica constantemente se um dispositivo USB foi conectado ou desconectado para atualizar a lista.
    :return none:
    """
    # TODO Arrumar para linux
    # Pega uma grande string contendo as placas
    placas_conectadas_anterior = listar_todas_placas_conectadas_cli()
    while 1:
        placas_conectadas = listar_todas_placas_conectadas_cli()
        print(f"Placas conectadas: {placas_conectadas}")
        if placas_conectadas_anterior != placas_conectadas:
            print("Portas atualizadas")
            objeto_principal.widget_central.criar_menu_portas()
            placas_conectadas_anterior = placas_conectadas
            sleep(1)


def procurar_placas(nome_placa):
    """
    Procura quais placas podem ser instaladas
    :return none:
    """

    # Seleciona o Arduino CLI correto pro sistema operacional
    if os.path.isfile('arduino-cli.exe'):
        arn_cli = os.path.abspath(os.path.join('.', 'arduino-cli.exe'))
    else:
        arn_cli = os.path.abspath(os.path.join('.', 'arduino-cli'))

    cmd = '"' + arn_cli + '"' + " board search " + nome_placa
    p = Popen(cmd, stdout=PIPE, stderr=PIPE, stdin=PIPE, shell=True)
    print(cmd)
    return p.stdout.read().decode()


def instalar_placa(nome_placa):
    """
    Instala uma nova placa ao core do arduino CLI.
    :return none:
    """
    # arduino-cli core install arduino:avr
    # Seleciona o Arduino CLI correto pro sistema operacional
    if os.path.isfile('arduino-cli.exe'):
        arn_cli = os.path.abspath(os.path.join('.', 'arduino-cli.exe'))
    else:
        arn_cli = os.path.abspath(os.path.join('.', 'arduino-cli'))

    cmd = '"' + arn_cli + '"' + " core install " + nome_placa
    p = Popen(cmd, stdout=PIPE, stderr=PIPE, stdin=PIPE, shell=True)
    print(cmd)
    # TODO avisar que a placa foi instalada com sucesso
    output = p.stdout.read()
    output += p.stderr.read()
    return output.decode()


def procurar_bibliotecas(nome_biblioteca):
    """
    Procura quais bibliotecas podem ser instaladas
    :return none:
    """
    # Seleciona o Arduino CLI correto pro sistema operacional
    if os.path.isfile('arduino-cli.exe'):
        arn_cli = os.path.abspath(os.path.join('.', 'arduino-cli.exe'))
    else:
        arn_cli = os.path.abspath(os.path.join('.', 'arduino-cli'))

    cmd = '"' + arn_cli + '"' + " lib search " + nome_biblioteca
    p = Popen(cmd, stdout=PIPE, stderr=PIPE, stdin=PIPE, shell=True)
    print(cmd)
    return p.stdout.read().decode()


def instalar_biblioteca(nome_biblioteca):
    """
    Instala uma nova biblioteca ao core do arduino CLI.
    :return none:
    """
    # arduino-cli core install arduino:avr
    # Seleciona o Arduino CLI correto pro sistema operacional
    if os.path.isfile('arduino-cli.exe'):
        arn_cli = os.path.abspath(os.path.join('.', 'arduino-cli.exe'))
    else:
        arn_cli = os.path.abspath(os.path.join('.', 'arduino-cli'))

    cmd = '"' + arn_cli + '"' + " lib install " + nome_biblioteca
    p = Popen(cmd, stdout=PIPE, stderr=PIPE, stdin=PIPE, shell=True)
    print(cmd)
    output = p.stdout.read()
    output += p.stderr.read()
    return output.decode()
