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
        self.widget_abas = None
        self.menu = None

        self.init_ui()

    def init_ui(self):
        layout = QGridLayout(self)
        layout.setRowStretch(0, 7.5)
        layout.setRowStretch(1, 2.5)
        layout.setColumnMinimumWidth(0, 60)
        layout.setSpacing(5)
        layout.setContentsMargins(0, 0, 0, 0)

        self.menu = Menu.Menu()
        layout.addWidget(self.menu, 0, 0, 2, 2)

        btn = QPushButton(self)
        btn.clicked.connect(self.nova_aba)

        self.widget_abas = QTabWidget(self)
        self.widget_abas.tabCloseRequested.connect(self.remover_aba)
        self.widget_abas.setTabsClosable(False)
        self.widget_abas.setCornerWidget(btn, Qt.TopRightCorner)
        layout.addWidget(self.widget_abas, 0, 1, 1, 2)

        self.nova_aba()

        log = QPlainTextEdit(self)
        log.setObjectName("log")
        log.setStyleSheet("border-radius:5px;background:#101010;margin-bottom:5px;margin-right:5px;")
        log.setDisabled(True)

        layout.addWidget(log, 1, 1, 1, 2)

        self.show()

    def remover_aba(self, index):
        if self.widget_abas.count() > 1:
            widget = self.widget_abas.widget(index)
            if widget is not None:
                widget.deleteLater()
            self.widget_abas.removeTab(index)
        if self.widget_abas.count() == 1:
            self.widget_abas.setTabsClosable(False)

    def nova_aba(self):
        if self.widget_abas.count() == 0:
            editor = EditorDeTexto.CodeEditor(tabs, False)
        else:
            editor = EditorDeTexto.CodeEditor(tabs, True)
        if self.widget_abas.count() == 1:
            self.widget_abas.setTabsClosable(True)
        text = editor.get_nome()
        highlight = DestaqueSintaxe.PythonHighlighter(editor.document())
        self.widget_abas.addTab(editor, text)
        if editor.get_nome() == "":
            self.remover_aba(self.widget_abas.count() - 1)
        else:
            self.widget_abas.setCurrentIndex(self.widget_abas.count() - 1)
