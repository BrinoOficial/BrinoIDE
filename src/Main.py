#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Br.ino Qt Main

Codigo da janela principal da IDE Br.ino
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
author: Mateus Berardo
author: Victor Rodrigues Pacheco
author: Gabriel Rodrigues Pacheco
"""

from json import loads, load
import os
import os.path
import sys
import webbrowser
from urllib.request import urlopen
import requests
import traceback
import threading

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QSplashScreen, QApplication, QMessageBox

import UI
from exceptions import UpdateException
import Rastreador
from integracao_arduino_cli import acompanha_portas_conectadas, get_caminho_padrao

# TODO Duplicado, resolver isso
versao = '3.0.7'
s = 3


def atualizar_linguas():
    versao_json = ""
    resultado = ""
    atualizadas = "Todas as línguas já estão atualizadas."
    try:
        with urlopen('http://brino.cc/brino/lib/ling/version.json') as json_versao:
            for linha in json_versao:
                versao_json += linha.decode('utf-8')
            versoes_linguas = loads(versao_json)
            arquivos = os.listdir(os.path.abspath('./recursos'))
            linguas = [nome_arquivo.replace('.json', '') for nome_arquivo in arquivos if nome_arquivo.endswith(".json")]
            for lingua in versoes_linguas['Linguas']:
                if lingua['ling'] in linguas:
                    lingua_local = load(open(os.path.join('recursos', lingua['ling'] + '.json')))
                    if int(lingua['version']) > int(lingua_local['version']):
                        with open(os.path.join('recursos', lingua['ling'] + '.json'), 'w') as f, urlopen(
                                'http://brino.cc/brino/lib/ling/' + lingua['ling'] + "/" + lingua[
                                    'ling'] + ".json") as json:
                            for linha in json:
                                f.write(linha.decode('utf-8'))
                            resultado += "JSON %s atualizado. " % str(lingua['ling'])
    except Exception as e:
        Rastreador.log_error("Houve um erro ao atualizar as línguas")
        raise UpdateException(e.args)
    return atualizadas if resultado == "" else resultado


def verificar_versao():
    """
    Verifica se ha uma nova versao disponivel no site.
    :return ha_atualizacao:
        Se ha ou nao atualizacoes disponiveis
    """
    ha_atualizacao = False
    versao_online = ''
    try:
        with urlopen('https://brino.cc/brino/versao.php') as versao_site:
            for linha in versao_site:
                versao_online += linha.decode('utf-8')

        versao_online = versao_online.split('.')
        versao_local = versao.split('.')
        for i in range(0, 3):
            if versao_online[i] > versao_local[i]:
                ha_atualizacao = True

    except Exception as e:
        Rastreador.log_error("Houve um erro ao verificar se há uma atualização online\n"+str(e))
    return ha_atualizacao


def install_excepthook():
    def my_excepthook(exctype, value, tb):
        erro_my_excepthook = ''.join(traceback.format_exception(exctype, value, tb))
        Rastreador.log_error("O Br.ino parou!")
        Rastreador.log_error(erro_my_excepthook)
        dialog = QMessageBox.question(None,
                                      'Isto é embaraçoso',
                                      "Infelizmente o Brino teve um problema e parou de funcionar. Você pode"
                                      + " nos enviar o relatório de erros?",
                                      QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if dialog == QMessageBox.Yes:
            # TODO Melhorar relatorio de erros do site
            # with open(os.path.join('recursos', 'completo.log'), 'rb') as f:
            #     try:
            #         # TODO Resolver problema de referencia
            #         r = requests.post('https://brino.cc/brino/receber_log.php', files={nome_arquivo: f})
            #     except requests.exceptions.RequestException as e:
            #         print(e)
            #     Rastreador.log_info(r.text)
            #     if "LOG enviado" in r.text:
            #         QMessageBox.question(None,
            #                              "Obrigado",
            #                              "O relatório foi enviado! Trabalharemos o mais rápido possível"
            #                              + " para resolver este problema!", QMessageBox.Ok, QMessageBox.Ok)
            #     else:
            #         QMessageBox.question(None,
            #                              "Poxa...",
            #                              "O relatório não pode ser enviado! Se puder, nos envie o arquivo por email."
            #                              + " O arquivo está dentro da pasta resources do diretório de instalação e se"
            #                              + " chama completo.log", QMessageBox.Ok, QMessageBox.Ok)
            pass
        sys.exit(-1)

    sys.excepthook = my_excepthook


def criar_pastas():
    """
    Verifica se a pasta de rascunhos brino e de bibliotecas existe, se nao existir elas sao criadas.
    """
    caminho_rascunhos = get_caminho_padrao()
    caminho_bibliotecas = get_caminho_padrao() + str("/Bibliotecas/")
    if not os.path.isdir(caminho_rascunhos):
        print("Criando as duas pastas")
        os.mkdir(caminho_rascunhos)
        os.mkdir(caminho_bibliotecas)
    elif not os.path.isdir(caminho_bibliotecas):
        print("Criando a pasta de bibliotecas")
        os.mkdir(caminho_bibliotecas)


if __name__ == '__main__':
    log = Rastreador.inicializar_log()
    app = QApplication(sys.argv)
    Rastreador.log_debug("APP Inicializado")
    splash_pix = QPixmap(os.path.join("recursos", "splash.png"))
    splash = QSplashScreen(splash_pix, Qt.WindowStaysOnTopHint)
    splash.setGeometry(200, 200, splash_pix.width(), splash_pix.height())
    splash.show()
    Rastreador.log_debug("Mostrando splash")
    app.processEvents()
    Rastreador.gerar_id_cliente()
    Rastreador.log_debug("ID gerado")
    install_excepthook()
    Rastreador.log_debug("Gerenciador de erros instalado")
    Rastreador.rastrear(Rastreador.ABERTURA)
    Rastreador.log_debug("Enviada Informação de abertura")
    with open(os.path.join("recursos", "stylesheet.txt")) as arquivo_stilo:
        stilo = arquivo_stilo.read()
        app.setStyleSheet(stilo)
    Rastreador.log_debug("Estilo Carregado")
    try:
        Rastreador.log_info(atualizar_linguas())
    except UpdateException as e:
        Rastreador.log_error(e)
    deve_atualizar = verificar_versao()
    Rastreador.log_debug("Verifacado se há atualizações. %s" % deve_atualizar)

    principal = UI.Principal()
    Rastreador.log_debug("Carregada tela principal")
    principal.widget_central.criar_menu_portas()
    Rastreador.log_debug("Menu portas iniciado")
    principal.show()
    Rastreador.log_debug("Aberta tela principal")
    if len(sys.argv) > 1:
        principal.widget_central.abrir(sys.argv[1], False)
        Rastreador.log_info("Aberto arquivo %s" % os.path.basename(sys.argv[1]))
    criar_pastas()
    splash.finish(principal)
    Rastreador.log_info("Fim da inicialização")

    # Cria e inicia um processo paralelo para acompanhar quando uma porta e conectada ou desconectada
    processo_acompanhar_portas_conectadas = threading.Thread(target=acompanha_portas_conectadas, args=(principal,))
    processo_acompanhar_portas_conectadas.daemon = True
    processo_acompanhar_portas_conectadas.start()

    if deve_atualizar:
        atual = QMessageBox().warning(None, 'Atualização',
                                      "Existe uma atualização disponível para o Brino!",
                                      QMessageBox.Ok | QMessageBox.Cancel)
        Rastreador.log_info("Há atualização")
        if atual == QMessageBox.Ok:
            Rastreador.log_info("Atualização Aceita")
            webbrowser.open("http://brino.cc/download.php", 1, True)
        elif atual == QMessageBox.Cancel:
            Rastreador.log_info("Atualização Recusada")

    sys.exit(app.exec_())
