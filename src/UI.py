#!/usr/bin/python
# -*- coding: utf-8 -*-

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QWidget, QGridLayout, QPlainTextEdit, QTabWidget, QPushButton)

import DestaqueSintaxe
import EditorDeTexto
import Menu

"""
Br.ino Qt UI

Interface base da IDE Br.ino
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

tabs = None


class Centro(QWidget):

    def __init__(self):
        super(Centro, self).__init__()
        self.tabs = QTabWidget(self)
        self.menu = Menu.Menu()

        self.init_ui()

    def init_ui(self):
        layout = QGridLayout(self)
        layout.setRowStretch(0, 7.5)
        layout.setRowStretch(1, 2.5)
        layout.setColumnMinimumWidth(0, 60)
        layout.setSpacing(5)
        layout.setContentsMargins(0, 0, 0, 0)

        layout.addWidget(self.menu, 0, 0, 2, 2)

        self.tabs.tabCloseRequested.connect(self.remover_aba)
        self.tabs.setTabsClosable(False)
        editor = EditorDeTexto.CodeEditor(self)
        editor.setStyleSheet("background:#252525;")
        self.tabs.addTab(editor, "Novo")
        btn = QPushButton(self)

        self.tabs.setCornerWidget(btn, Qt.TopRightCorner)
        btn.clicked.connect(self.nova_aba)
        global tabs
        tabs = self.tabs

        highlight = DestaqueSintaxe.PythonHighlighter(editor.document())
        layout.addWidget(self.tabs, 0, 1, 1, 2)

        log = QPlainTextEdit(self)
        log.setStyleSheet("background:#000000; margin-bottom: 5px; margin-right: 5px;")
        log.setDisabled(True)
        layout.addWidget(log, 1, 1, 1, 2)

        self.show()

    def remover_aba(self, index):
        if self.tabs.count() > 1:
            widget = self.tabs.widget(index)
            if widget is not None:
                widget.deleteLater()
            self.tabs.removeTab(index)
        if self.tabs.count() == 1:
            self.tabs.setTabsClosable(False)

    def novo(arg, perguntar=True):
        print("novando")
        print perguntar
        global caminho_padrao, caminho
        if perguntar:
            text, ok = QInputDialog.getText(None, "Novo arquivo", "Nome do rascunho:")
            if ok and text != "":
                caminho = os.path.join(caminho_padrao, text, text + ".brpp")
                UI.Centro.nova_aba(UI.Centro.instance, text=text)
                print(caminho)
            elif not ok:
                return
            else:
                print("nome vazio wtf")
        else:
            caminho_padrao = os.path.expanduser("~")
            docu = re.compile("Documen.*")
            pastas = os.listdir(caminho_padrao)
            documentos = filter(docu.match, pastas)
            caminho_padrao = os.path.join(caminho_padrao, documentos[0], "RascunhosBrino")
        caminho = ""

    def nova_aba(self, text="Novo"):
        if self.tabs.count() == 1:
            self.tabs.setTabsClosable(True)
        editor = EditorDeTexto.CodeEditor(tabs)
        editor.setStyleSheet("background:#252525;")
        tabs.addTab(editor, "Novo")

