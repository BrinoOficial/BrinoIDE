#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Br.ino Qt Main

Codigo da janela principal da IDE Br.ino
em PyQt5 (python 2.7)

    setaCima.png, setaBaixo.png, setaDireita.png e setaEsquerda.png 
    made by Dave Gandy
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
contributor: Victor Rodrigues Pacheco
email: victor.pacheco@brino.cc
"""

import os
import re
import sys

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QApplication, QAction

import GerenciadorDeArquivos
import GerenciadorDeCodigo
import GerenciadorDeLinguas
import MonitorSerial
import UI

versao = '3.0.0'

monitor = 3

class Principal(QMainWindow):

    def __init__(self):
        super(Principal, self).__init__()

        self.acao_novo = QAction('&Novo', self)
        self.acao_abrir = QAction('Abrir', self)
        self.acao_exemplos = QAction('Exemplos', self)
        self.acao_sair = QAction('Sair', self)
        self.acao_salvar = QAction('&Salvar', self)
        self.acao_salvar_como = QAction('Salvar como', self)
        self.acao_comentar_linha = QAction('Comentar linha', self)
        self.acao_achar = QAction('Achar...', self)
        self.acao_achar_e_substituir = QAction('Achar e substituir', self)
        self.acao_ir_para_linha = QAction('Ir para linha', self)
        self.acao_placa = QAction('Placa', self)
        self.acao_porta = QAction('Porta', self)
        self.acao_lingua = QAction('Lingua', self)
        self.acao_monitor_serial = QAction('Monitor serial', self)
        self.acao_verificar = QAction('Verificar', self)
        self.acao_verificar_e_carregar = QAction('Verificar e carregar', self)

        self.widget_central = UI.Centro(self)

        self.init_ui()

    def init_ui(self):
        self.criar_barra_menu()

        self.setCentralWidget(self.widget_central)

        self.setGeometry(100, 50, 500, 550)
        self.setMinimumSize(500, 520)
        self.setWindowTitle('Br.ino ' + versao)
        self.setWindowIcon(QIcon(os.path.join('recursos', 'logo.png')))
        self.show()

    def criar_acoes(self):
        """
            Define as funcoes de resposta as acoes e conecta elas. Define atalhos de teclado
        """
        self.acao_sair.setShortcut('Ctrl+Q')
        self.acao_sair.triggered.connect(self.close)

        self.acao_novo.setShortcut("Ctrl+N")
        self.acao_novo.triggered.connect(self.widget_central.nova_aba)

        self.acao_abrir.setShortcut('Ctrl+O')
        self.acao_abrir.triggered.connect(self.widget_central.abrir)

        self.acao_exemplos.triggered.connect(GerenciadorDeArquivos.exemplos)

        self.acao_salvar.setShortcut('Ctrl+S')
        self.acao_salvar.triggered.connect(self.widget_central.salvar)

        self.acao_salvar_como.setShortcut('Ctrl+Shift+S')
        self.acao_salvar_como.triggered.connect(self.widget_central.salvar_como)

        self.acao_comentar_linha.setShortcut('Ctrl+/')
        self.acao_comentar_linha.triggered.connect(GerenciadorDeCodigo.comentar_linha)

        self.acao_achar.setShortcut('Ctrl+F')
        self.acao_achar.triggered.connect(GerenciadorDeCodigo.achar)

        self.acao_achar_e_substituir.setShortcut('Ctrl+H')
        self.acao_achar_e_substituir.triggered.connect(GerenciadorDeCodigo.achar_e_substituir)

        self.acao_ir_para_linha.setShortcut('Ctrl+L')
        self.acao_ir_para_linha.triggered.connect(GerenciadorDeCodigo.ir_para_linha)

        self.acao_placa.triggered.connect(GerenciadorDeCodigo.placa)

        self.acao_porta.triggered.connect(GerenciadorDeCodigo.porta)

        self.acao_lingua.triggered.connect(GerenciadorDeLinguas.lingua)

        self.acao_monitor_serial.setShortcut('Ctrl+Shift+M')
        self.acao_monitor_serial.triggered.connect(MonitorSerial.monitor_serial)
        self.acao_monitor_serial.triggered.connect(self.abrir_serial)

        self.acao_verificar.setShortcut('Ctrl+R')
        self.acao_verificar.triggered.connect(GerenciadorDeCodigo.verificar)

        self.acao_verificar_e_carregar.setShortcut('Ctrl+U')
        self.acao_verificar_e_carregar.triggered.connect(GerenciadorDeCodigo.verificar_e_carregar)

    def criar_barra_menu(self):
        self.criar_acoes()

        barra_menu = self.menuBar()
        barra_menu.setNativeMenuBar(False)
        menu_arquivo = barra_menu.addMenu('Arquivo')
        menu_arquivo.addAction(self.acao_novo)
        menu_arquivo.addAction(self.acao_abrir)
        menu_exemplos = menu_arquivo.addMenu('Exemplos')
        self.adicionar_exemplos(menu_exemplos)
        menu_arquivo.addAction(self.acao_salvar)
        menu_arquivo.addAction(self.acao_salvar_como)
        menu_arquivo.addAction(self.acao_sair)

        menu_editar = barra_menu.addMenu('Editar')
        menu_editar.addAction(self.acao_comentar_linha)
        menu_editar.addAction(self.acao_achar)
        menu_editar.addAction(self.acao_achar_e_substituir)
        menu_editar.addAction(self.acao_ir_para_linha)

        menu_ferramentas = barra_menu.addMenu('Ferramentas')
        menu_placa = menu_ferramentas.addMenu('Placa')
        menu_porta = menu_ferramentas.addMenu('Porta')
        menu_ferramentas.addAction(self.acao_lingua)
        menu_ferramentas.addAction(self.acao_monitor_serial)

        menu_rascunho = barra_menu.addMenu('Rascunho')
        menu_rascunho.addAction(self.acao_verificar)
        menu_rascunho.addAction(self.acao_verificar_e_carregar)

    def adicionar_exemplos(self, menu):
        # TODO ler exemplos e adiciona-los ao menu exemplos
        pass

    def abrir_serial(self):
        monitor.show()


def get_caminho_padrao():
    caminho_padrao = os.path.expanduser("~")
    docu = re.compile("Documen.*")
    pastas = os.listdir(caminho_padrao)
    documentos = filter(docu.match, pastas)
    return os.path.join(caminho_padrao, documentos[0], "RascunhosBrino")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    with open(os.path.join("recursos", "stylesheet.txt")) as arquivo_stilo:
        stilo = arquivo_stilo.read()
        app.setStyleSheet(stilo)
    monitor = MonitorSerial.MonitorSerial()
    principal = Principal()
    principal.show()
    sys.exit(app.exec_())
