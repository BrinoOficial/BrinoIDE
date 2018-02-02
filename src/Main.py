#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
from PyQt4 import QtGui

import GerenciadorDeArquivos
import GerenciadorDeCodigo
import GerenciadorDeExemplos
import GerenciadorDeLinguas
import GerenciadorDeTexto
import MonitorSerial
import UI

"""
Br.ino Qt Main

Codigo da janela principal da IDE Br.ino
em PyQt4 (python 2.7)

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

versao = '3.0.0'


class Principal(QtGui.QMainWindow):

    def __init__(self):
        super(Principal, self).__init__()

        self.acao_novo = 0
        self.acao_abrir = 0
        self.acao_exemplos = 0
        self.acao_sair = 0
        self.acao_salvar = 0
        self.acao_salvar_como = 0
        self.acao_comentar_linha = 0
        self.acao_achar = 0
        self.acao_achar_e_substituir = 0
        self.acao_ir_para_linha = 0
        self.acao_placa = 0
        self.acao_porta = 0
        self.acao_lingua = 0
        self.acao_monitor_serial = 0
        self.acao_verificar = 0
        self.acao_verificar_e_carregar = 0

        self.init_ui()

    def init_ui(self):
        self.criar_barra_menu()

        self.setCentralWidget(UI.Centro())

        self.setGeometry(300, 300, 500, 550)
        self.setWindowTitle('Br.ino ' + versao)
        self.setWindowIcon(QtGui.QIcon(os.path.join('recursos','logo.png')))
        self.show()

    def criar_acoes(self):
        acao_sair = QtGui.QAction('Sair', self)
        acao_sair.setStatusTip('Sair da IDE do Br.ino')
        acao_sair.triggered.connect(self.close)
        self.acao_sair = acao_sair

        acao_novo = QtGui.QAction('&Novo', self)
        acao_novo.setShortcut("Ctrl+N")
        acao_novo.triggered.connect(GerenciadorDeArquivos.novo)
        self.acao_novo = acao_novo

        acao_abrir = QtGui.QAction('Abrir', self)
        acao_abrir.setShortcut('Ctrl+O')
        acao_abrir.triggered.connect(GerenciadorDeArquivos.abrir)
        self.acao_abrir = acao_abrir

        acao_exemplos = QtGui.QAction('Exemplos', self)
        acao_exemplos.triggered.connect(GerenciadorDeArquivos.exemplos)
        self.acao_exemplos = acao_exemplos

        acao_salvar = QtGui.QAction('&Salvar', self)
        acao_salvar.setShortcut('Ctrl+S')
        acao_salvar.triggered.connect(GerenciadorDeArquivos.salvar)
        self.acao_salvar = acao_salvar

        acao_salvar_como = QtGui.QAction('Salvar como', self)
        acao_salvar_como.setShortcuts('Ctrl+B')
        acao_salvar_como.triggered.connect(GerenciadorDeArquivos.salvar_como)
        self.acao_salvar_como = acao_salvar_como

        acao_comentar_linha = QtGui.QAction('Comentar linha', self)
        acao_comentar_linha.setShortcuts('Ctrl+/')
        acao_comentar_linha.triggered.connect(GerenciadorDeCodigo.comentar_linha)
        self.acao_comentar_linha = acao_comentar_linha

        acao_achar = QtGui.QAction('Achar...', self)
        acao_achar.setShortcuts('Ctrl+F')
        acao_achar.triggered.connect(GerenciadorDeCodigo.achar)
        self.acao_achar = acao_achar

        acao_achar_e_substituir = QtGui.QAction('Achar e substituir', self)
        acao_achar_e_substituir.setShortcuts('Ctrl+H')
        acao_achar_e_substituir.triggered.connect(GerenciadorDeCodigo.achar_e_substituir)
        self.acao_achar_e_substituir = acao_achar_e_substituir

        acao_ir_para_linha = QtGui.QAction('Ir para linha', self)
        acao_ir_para_linha.setShortcuts('Ctrl+L')
        acao_ir_para_linha.triggered.connect(GerenciadorDeCodigo.ir_para_linha)
        self.acao_ir_para_linha = acao_ir_para_linha

        acao_placa = QtGui.QAction('Placa', self)
        acao_placa.triggered.connect(GerenciadorDeCodigo.placa)
        self.acao_placa = acao_placa

        acao_porta = QtGui.QAction('Porta', self)
        acao_porta.triggered.connect(GerenciadorDeCodigo.porta)
        self.acao_porta = acao_porta

        acao_lingua = QtGui.QAction('Lingua', self)
        acao_lingua.triggered.connect(GerenciadorDeLinguas.lingua)
        self.acao_lingua = acao_lingua

        acao_monitor_serial = QtGui.QAction('Monitor serial', self)
        acao_monitor_serial.setShortcuts('Ctrl+Shift+M')
        acao_monitor_serial.triggered.connect(MonitorSerial.monitor_serial)
        self.acao_monitor_serial = acao_monitor_serial

        acao_verificar = QtGui.QAction('Verificar', self)
        acao_verificar.setShortcuts('Ctrl+R')
        acao_verificar.triggered.connect(GerenciadorDeCodigo.verificar)
        self.acao_verificar = acao_verificar

        acao_verificar_e_carregar = QtGui.QAction('Verificar e carregar', self)
        acao_verificar_e_carregar.setShortcuts('Ctrl+U')
        acao_verificar_e_carregar.triggered.connect(GerenciadorDeCodigo.verificar_e_carregar)
        self.acao_verificar_e_carregar = acao_verificar_e_carregar




    def criar_barra_menu(self):
        self.criar_acoes()

        barra_menu = self.menuBar()
        menu_arquivo = barra_menu.addMenu('&Arquivo')
        menu_arquivo.addAction(self.acao_novo)
        menu_arquivo.addAction(self.acao_abrir)
        menu_arquivo.addAction(self.acao_exemplos)
        menu_arquivo.addAction(self.acao_salvar)
        menu_arquivo.addAction(self.acao_salvar_como)

        menu_editar = barra_menu.addMenu('&Editar')
        menu_editar.addAction(self.acao_comentar_linha)
        menu_editar.addAction(self.acao_achar)
        menu_editar.addAction(self.acao_achar_e_substituir)
        menu_editar.addAction(self.acao_ir_para_linha)

        menu_ferramentas = barra_menu.addMenu('Ferramentas')
        menu_ferramentas.addAction(self.acao_placa)
        menu_ferramentas.addAction(self.acao_porta)
        menu_ferramentas.addAction(self.acao_lingua)
        menu_ferramentas.addAction(self.acao_monitor_serial)

        menu_rascunho = barra_menu.addMenu('Rascunho')
        menu_rascunho.addAction(self.acao_verificar)
        menu_rascunho.addAction(self.acao_verificar_e_carregar)


def main():
    app = QtGui.QApplication(sys.argv)
    principal = Principal()
    app.setStyleSheet("""QMainWindow {
                             background: '#252525';
                         }
                         QMenu{
                             background: '#252525';
                         }
                         QMenu::item {
                             background: '#252525';
                         } 
                         QMenu::item:selected{
                             background: '#101010';
                         }
                         QMenuBar {
                             background: '#252525';
                         }
                         QMenuBar::item {
                             background: '#252525';
                         } 
                         QMenuBar::item:selected{
                             background: '#101010';
                         }
                         QPlainTextEdit{
                             background: '#252525';
                             border: None;
                             border-radius: 6px;
                         }""")
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
