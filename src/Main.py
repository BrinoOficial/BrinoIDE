#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from PyQt4 import QtGui

import GerenciadorDeArquivos
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
     
author: Mateus Berardo
website: brino.cc
email: mateus.berardo@brino.cc
"""

versao = '3.0.0'


class Principal(QtGui.QMainWindow):

    def __init__(self):
        super(Principal, self).__init__()
        self.acao_abrir = 0
        self.acao_novo = 0
        self.acao_sair = 0
        self.init_ui()

    def init_ui(self):
        self.criar_acoes()

        self.criar_barra_menu()

        container = UI.Centro()
        self.setCentralWidget(container)

        self.setGeometry(300, 300, 500, 550)
        self.setWindowTitle('Br.ino ' + versao)
        self.show()

    def criar_acoes(self):
        acao_sair = QtGui.QAction('Exit', self)
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

    def criar_barra_menu(self):
        barra_menu = self.menuBar()
        menu_arquivo = barra_menu.addMenu('&Arquivo')
        menu_arquivo.addAction(self.acao_novo)
        menu_arquivo.addAction(self.acao_abrir)


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
                         QTextEdit{
                             background: '#474747';
                             border: None;
                             border-radius: 6px;
                         }""")
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
