#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Br.ino Qt Main

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

from json import loads, load
import os
import sys
import webbrowser
from urllib.request import urlopen
import uuid
import requests
import traceback
import re

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QSplashScreen, QMainWindow, QApplication, QAction, QMenu, QStatusBar, QMessageBox, QLabel

import GerenciadorDeCodigo
import GerenciadorDeLinguas
import MonitorSerial
import Preferencias
import UI
from exceptions import UpdateException
import Rastreador

versao = '3.0.6'
caminho_padrao = ''
monitor = 3


class Principal(QMainWindow):

    def __init__(self):
        super(Principal, self).__init__()

        # Define as acoes
        self.acao_novo = QAction('&Novo', self)
        self.acao_abrir = QAction('Abrir', self)
        self.acao_abrir_arduino = QAction('Abrir Traducao', self)
        self.acao_exemplos = QAction('Exemplos', self)
        self.acao_sair = QAction('Sair', self)
        self.acao_fechar_aba = QAction('Fechar aba', self)
        self.acao_salvar = QAction('&Salvar', self)
        self.acao_salvar_como = QAction('Salvar como', self)
        self.acao_comentar_linha = QAction('Comentar linha', self)
        self.acao_achar = QAction('Achar...', self)
        self.acao_achar_e_substituir = QAction('Achar e substituir', self)
        self.acao_ir_para_linha = QAction('Ir para linha', self)
        self.acao_placa = QAction('Placa', self)
        self.acao_porta = QAction('Porta', self)
        self.acao_lingua = QAction('Lingua', self)
        self.acao_instalar_biblioteca = QAction('Instalar biblioteca', self)
        self.acao_monitor_serial = QAction('Monitor serial', self)
        self.acao_verificar = QAction('Verificar', self)
        self.acao_verificar_e_carregar = QAction('Verificar e carregar', self)
        self.menu_placas = QMenu('Placa')
        self.menu_portas = QMenu('Porta')
        self.menu_exemplos = QMenu('Exemplos')
        self.barra_de_status = QStatusBar()

        self.widget_central = UI.Centro(self)

        self.criar_barra_menu()

        self.init_ui()

    def init_ui(self):
        self.setStatusBar(self.barra_de_status)
        if Preferencias.get("board") is None:
            Preferencias.set("board", "uno")
        if Preferencias.get("serial.port") is None:
            Preferencias.set("serial.port", "COM1")
        self.placa_porta_label = QLabel(Preferencias.get("board") + " na " + Preferencias.get("serial.port"))
        self.barra_de_status.addPermanentWidget(self.placa_porta_label)

        self.setCentralWidget(self.widget_central)

        self.setGeometry(100, 50, 500, 550)
        self.setMinimumSize(500, 520)
        self.setWindowTitle('Br.ino ' + versao)
        self.setWindowIcon(QIcon(os.path.join('recursos', 'logo.png')))

        self.show()

    def criar_acoes(self):
        """
        Define as funcoes de resposta as acoes e conecta elas. Define atalhos de teclado
        :return:
            None
        """
        self.acao_sair.setShortcut('Ctrl+Q')
        self.acao_sair.setStatusTip('Sair da IDE do Br.ino')
        self.acao_sair.triggered.connect(self.close)
        self.acao_sair.triggered.connect(monitor.close)

        self.acao_fechar_aba.setShortcut('Ctrl+W')
        self.acao_fechar_aba.setStatusTip('Fechar aba atual')
        self.acao_fechar_aba.triggered.connect(self.widget_central.remover_aba)

        self.acao_novo.setShortcut("Ctrl+N")
        self.acao_novo.triggered.connect(self.widget_central.nova_aba)
        self.acao_novo.setStatusTip("Criar novo arquivo")

        self.acao_abrir.setShortcut('Ctrl+O')
        self.acao_abrir.triggered.connect(self.widget_central.abrir)
        self.acao_abrir.setStatusTip("Abrir arquivo")

        self.acao_abrir_arduino.setShortcut('Ctrl+T')
        self.acao_abrir_arduino.triggered.connect(self.widget_central.abrir_traducao)
        self.acao_abrir.setStatusTip("Abrir Tradução")

        self.acao_salvar.setShortcut('Ctrl+S')
        self.acao_salvar.triggered.connect(self.widget_central.salvar)
        self.acao_salvar.setStatusTip("Salvar arquivo")

        self.acao_salvar_como.setShortcut('Ctrl+Shift+S')
        self.acao_salvar_como.triggered.connect(self.widget_central.salvar_como)
        self.acao_salvar_como.setStatusTip("Salvar arquivo como")

        self.acao_comentar_linha.setShortcut('Ctrl+/')
        self.acao_comentar_linha.triggered.connect(self.widget_central.comentar_linha)
        self.acao_comentar_linha.setStatusTip("Comentar linha")

        self.acao_achar.setShortcut('Ctrl+F')
        self.acao_achar.triggered.connect(self.widget_central.achar)
        self.acao_achar.setStatusTip("Achar...")

        self.acao_achar_e_substituir.setShortcut('Ctrl+H')
        self.acao_achar_e_substituir.triggered.connect(self.widget_central.achar_e_substituir)
        self.acao_achar_e_substituir.setStatusTip("Achar e substituir...")

        self.acao_ir_para_linha.setShortcut('Ctrl+L')
        self.acao_ir_para_linha.triggered.connect(GerenciadorDeCodigo.ir_para_linha)
        self.acao_ir_para_linha.setStatusTip("Ir para linha...")

        self.acao_lingua.triggered.connect(GerenciadorDeLinguas.lingua)
        self.acao_lingua.setStatusTip("Opções de língua")

        self.acao_instalar_biblioteca.triggered.connect(self.widget_central.instalar_biblioteca)
        self.acao_instalar_biblioteca.setStatusTip("Instalar bilioteca")

        self.acao_monitor_serial.setShortcut('Ctrl+Shift+M')
        self.acao_monitor_serial.triggered.connect(self.abrir_serial)
        self.acao_monitor_serial.setStatusTip("Abrir monitor serial")

        self.acao_verificar.setShortcut('Ctrl+R')
        self.acao_verificar.triggered.connect(self.widget_central.compilar)
        self.acao_verificar.setStatusTip("Verificar código")

        self.acao_verificar_e_carregar.setShortcut('Ctrl+U')
        self.acao_verificar_e_carregar.triggered.connect(self.enviar_codigo)
        self.acao_verificar_e_carregar.setStatusTip("Verificar e carregar código")

    def criar_barra_menu(self):
        """
        Cria a barra menu e adiciona as funcoes nela
        :return:
            None
        """
        self.criar_acoes()

        barra_menu = self.menuBar()
        barra_menu.setNativeMenuBar(False)
        menu_arquivo = barra_menu.addMenu('Arquivo')
        menu_arquivo.addAction(self.acao_novo)
        menu_arquivo.addAction(self.acao_abrir)
        menu_arquivo.addAction(self.acao_abrir_arduino)
        menu_arquivo.addMenu(self.menu_exemplos)
        menu_arquivo.addAction(self.acao_salvar)
        menu_arquivo.addAction(self.acao_salvar_como)
        menu_arquivo.addAction(self.acao_fechar_aba)
        menu_arquivo.addAction(self.acao_sair)

        menu_editar = barra_menu.addMenu('Editar')
        menu_editar.addAction(self.acao_comentar_linha)
        menu_editar.addAction(self.acao_achar)
        menu_editar.addAction(self.acao_achar_e_substituir)
        menu_editar.addAction(self.acao_ir_para_linha)

        self.menu_ferramentas = barra_menu.addMenu('Ferramentas')
        self.menu_ferramentas.aboutToShow.connect(self.widget_central.criar_menu_portas)
        self.menu_ferramentas.addMenu(self.menu_placas)
        self.menu_ferramentas.addMenu(self.menu_portas)
        self.menu_ferramentas.addAction(self.acao_lingua)
        self.menu_ferramentas.addAction(self.acao_monitor_serial)
        self.menu_ferramentas.addAction(self.acao_instalar_biblioteca)

        menu_rascunho = barra_menu.addMenu('Rascunho')
        menu_rascunho.addAction(self.acao_verificar)
        menu_rascunho.addAction(self.acao_verificar_e_carregar)

    def abrir_serial(self):
        """
        Abre o monitor serial ou indica que a porta nao esta disponivel
        :return:
            None
        """

        # Verifica se jah hah um monitor aberto e o fecha
        if monitor.isVisible():
            monitor.close()
        if monitor.conectar(Preferencias.get("serial.port")):
            monitor.show()
            Rastreador.log_info("Monitor Serial aberto")
        else:
            QMessageBox("Erro", QMessageBox.Warning, "A porta selecionada não está disponível",
                        QMessageBox.NoButton, self).show()
            Rastreador.log_error("Porta Serial solicitada não disponível")

    def enviar_codigo(self):
        """
        Fecha o monitor serial, compila e carrega o codigo da aba atual
        :return:
            None
        """
        Rastreador.log_info("Compilando e Carregando")
        reconectar = monitor.desconectar()
        self.widget_central.upload()
        Rastreador.log_info("Fim do upload")
        if reconectar:
            Rastreador.log_info("Monitor Serial fechado e reconectando")
            self.abrir_serial()
            Rastreador.log_info("Monitor Serial reconectado")

    def closeEvent(self, close_event):
        """
        Fecha o programa, mas antes verifica se os arquivos foram salvos
        :param close_event:
        :return:
        """
        if self.widget_central.widget_abas.widget(0).caminho == 0:
            num_examinar = 1
        else:
            num_examinar = 0
        for num_arquivo in range(self.widget_central.widget_abas.count() - num_examinar):
            if not self.widget_central.remover_aba(num_examinar, True):
                close_event.ignore()
                return
        Rastreador.log_info("Encerrando o Br.ino")
        monitor.close()
        Rastreador.log_info("Monitor serial encerrado")
        Rastreador.rastrear(Rastreador.FECHAMENTO)
        Rastreador.log_info("Rastreado fechamento")
        Preferencias.gravar_preferencias()
        Rastreador.log_info("Preferências registradas, encerrando...")
        close_event.accept()


def get_caminho_padrao():
    """
    Pega o caminho padrao ate a pasta de RascunhosBrino
    :return:
        Caminho padrao
    """
    global caminho_padrao
    caminho_padrao = os.path.expanduser("~")
    docu = re.compile("Documen.*")
    pastas = os.listdir(caminho_padrao)
    documentos = list(filter(docu.match, pastas))
    if documentos is None:
        documentos[0] = "Documentos"
    return os.path.join(caminho_padrao, documentos[0], "RascunhosBrino")


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


def gerar_id_cliente():
    """
    Verifica se no arquivo de preferências há um id único para o cliente. Caso contrário, gera um.
    :return:
        None
    """
    # Comente essas linhas para teste, descomente para produção
    if Preferencias.get("id_cliente") == "5ecd82bd-bea5-461e-b153-023626168f8e":
        Rastreador.log_info("Não há ID registrado, primeiro uso")
        idc = uuid.uuid4()
        Preferencias.set("id_cliente", str(idc))
        Rastreador.log_info("id definido como:", Preferencias.get("id_cliente"))


def verificar_versao():
    """
    Verifica se ha uma nova versao disponivel no site.
    :return ha_atualizacao:
        Se ha ou nao atualizacoes disponiveis
    """
    ha_atualizacao = False
    versao_online = ''
    try:
        with urlopen('http://brino.cc/brino/versao.php') as versao_site:
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
        s = ''.join(traceback.format_exception(exctype, value, tb))
        Rastreador.log_error("O Br.ino parou!")
        Rastreador.log_error(s)
        dialog = QMessageBox.question(None,
                                      'Isto é embaraçoso',
                                      "Infelizmente o Brino teve um problema e parou de funcionar. Você pode"
                                      + " nos enviar o relatório de erros?",
                                      QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if dialog == QMessageBox.Yes:
            with open(os.path.join('recursos', 'completo.log'), 'rb') as f:
                nome_arquivo = '%s.log' % Preferencias.get("id_cliente")
                try:
                    r = requests.post('https://brino.cc/brino/receber_log.php', files={nome_arquivo: f})
                except requests.exceptions.RequestException as e:
                    print(e)
                Rastreador.log_info(r.text)
                if "LOG enviado" in r.text:
                    QMessageBox.question(None,
                                         "Obrigado",
                                         "O relatório foi enviado! Trabalharemos o mais rápido possível"
                                         + " para resolver este problema!", QMessageBox.Ok, QMessageBox.Ok)
                else:
                    QMessageBox.question(None,
                                         "Poxa...",
                                         "O relatório não pode ser enviado! Se puder, nos envie o arquivo por email."
                                         + " O arquivo está dentro da pasta resources do diretório de instalação e se"
                                         + " chama completo.log", QMessageBox.Ok, QMessageBox.Ok)
        sys.exit(-1)

    sys.excepthook = my_excepthook


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
    Preferencias.init()
    Rastreador.log_debug("Preferencias carregadas")
    gerar_id_cliente()
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
    monitor = MonitorSerial.MonitorSerial()
    Rastreador.log_debug("Carregado monitor serial")
    principal = Principal()
    Rastreador.log_debug("Carregada tela principal")
    principal.show()
    Rastreador.log_debug("Aberta tela principal")
    if len(sys.argv) > 1:
        principal.widget_central.abrir(sys.argv[1], False)
        Rastreador.log_info("Aberto arquivo %s" % os.path.basename(sys.argv[1]))

    splash.finish(principal)
    Rastreador.log_info("Fim da inicialização")
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

