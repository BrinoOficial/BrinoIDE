#!/usr/bin/python
# -*- coding: utf-8 -*-

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

import sys
from subprocess import Popen, PIPE

import Preferencias


def novo_uploader(placa_alvo, porta, nao_existe_porta):
    """
    Caso seja um upload sem prefs
    :param placa_alvo:
        Placa alvo
    :param porta:
        Porta alvo
    :param nao_existe_porta:
        Porta nao existente ou invalida
    :return:
    """
    if nao_existe_porta:
        return UploaderSerial(nao_existe_porta)
    if porta is not None and porta.get_protocolo() == "network":
        if porta.get_prefs().get("ssh_upload") == "no":
            pass
            # TODO Network Uploader
        # TODO SSH Uploader


def get_uploader_por_preferencias():
    """
    upload com prefs
    :return:
        None
    """
    # TODO
    pass


class UploaderSerial():
    def __init__(self, nao_existe_porta=False):
        """
        Init do uploader
        :param nao_existe_porta:
            Caso de porta invalida ou inexistente
        """
        self.verbose = Preferencias.get("upload.verbose")
        self.verificar_carregar = Preferencias.get("upload.verify")
        self.error = ""
        self.erro_nao_encontrado = False
        self.nao_existe_porta = nao_existe_porta

    # sucesso = Uploader.upload_usando_preferencias(self, caminho, caminho_temp, nome, usando_programador)

    def upload_usando_preferencias(self, parent, caminho_temp, nome):
        """
        Faz upload de acordo com as preferencias
        :param parent:
            Funcao pai
        :param caminho_temp:
            Caminho temporario
        :param nome:
            Nome do codigo
        :return:
            None
        """
        plataforma_alvo = parent.get_plataforma_alvo()
        prefs = Preferencias.get_mapa()
        preferencias_placa = parent.get_preferencias_placa()
        if preferencias_placa is not None:
            prefs.update(preferencias_placa)
        tool = prefs["upload.tool"]
        if tool.__contains__(":"):
            separado = tool.split(":", 2)
            plataforma_alvo = parent.get_plataforma_alvo_do_pacote(separado[0])
            tool = separado[1]
        prefs.update(plataforma_alvo.get_ferramenta(tool))
        # TODO upload com programador]
        if self.nao_existe_porta:
            prefs["build.path"] = caminho_temp
            prefs["build.project_name"] = nome
            prefs['upload.verbose'] = prefs.get("upload.params.quiet")
            # TODO upload verify
            resultado = False
            padrao = prefs.get("upload.pattern")
            cmd = formatar_e_dividir(padrao, prefs, True)
            # TODO executar comando e retornar

        t = prefs.get("upload.use_1200bps_touch", None)
        fazer_toque = t is not None and t
        t = prefs.get("upload.wait_for_upload_port", None)
        esperar_porta_upload = t is not None and t
        porta_selecionada = prefs.get("serial.port", None)
        if porta_selecionada is None:
            # TODO erro e retornar
            pass
        if fazer_toque:
            # TODO
            pass
        prefs['build.path'] = caminho_temp
        prefs['build.project_name'] = nome
        prefs['upload.verbose'] = prefs.get("upload.params.quiet")
        # TODO verbose, verify upload
        padrao = prefs["upload.pattern"]
        cmd = formatar_e_dividir(padrao, prefs, True)
        cmd = " ".join(cmd)
        print(cmd)
        p = Popen(cmd, stdout=PIPE, stderr=PIPE, stdin=PIPE, shell=True)
        output = p.stdout.read()
        output += p.stderr.read()
        if not output:
            parent.log.insertPlainText("Carregado!")
        else:
            try:
                decodificada = output.decode('utf8')
            except UnicodeDecodeError:
                utf8_string = str(output.decode('latin1').encode('utf-8'))
                decodificada = utf8_string.replace("b'", "").replace("'", "").replace("\\xc3\\xa3",'ã').replace("\\r", '').replace('\\n', '').replace("\\", '')
            finally:
                parent.log.insertPlainText(decodificada)


def formatar_e_dividir(src, dictio, recursivo):
    """
    TODO
    :param src:
    :param dictio:
    :param recursivo:
    :return:
    """
    res = ""
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
            arg_escapado += s + " ";
            continue
        arg_escapado += s[0:len(s) - 1]
        if not len(arg_escapado.strip()) == 0 or arg_vazios:
            res.append(arg_escapado)
            char_escapador = None
    if char_escapador is not None:
        print("Erro")
    return res
