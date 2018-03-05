#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Br.ino Qt BoasVindas

Codigo da aba de boas vindas da IDE Br.ino
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

import os
import webbrowser

from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel, QSizePolicy, QVBoxLayout


class BoasVindas(QWidget):
    def __init__(self, parent):
        super(BoasVindas, self).__init__(parent)
        self.caminho = 0
        self.layout = QGridLayout(self)
        self.parent = parent
        self.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.layout.setColumnStretch(0, 1)
        # Onde vai entrar o achar
        # self.layout.setColumnStretch(1, 12)
        self.layout.setRowStretch(0, 1)
        self.layout.setRowStretch(1, 1)
        self.layout.setSpacing(5)
        self.setContentsMargins(0, 0, 0, 0)
        self.layout.addWidget(Mascote(self), 0, 0)
        self.setAutoFillBackground(True)
        self.itens = QVBoxLayout(self)
        self.popular_itens()
        self.salvo = True

    def popular_itens(self):
        novo = Item(self, self.parent.nova_aba, "Rascunho em Branco", "Crie um novo rascunho do zero",
                    os.path.join('recursos', 'novoArquivo.png'))
        aprender_mais = Item(self, self.abrir_site, "Não sabe como começar?",
                             "Visite nosso site para ler um de nossos tutoriais!", "")
        self.layout.addLayout(self.itens, 0, 0)
        self.itens.addWidget(novo)
        self.itens.addWidget(aprender_mais)
        self.setFixedHeight(300)

    @staticmethod
    def abrir_site():
        webbrowser.open("http://brino.cc/tutoriais.php", 1, True)

    def get_caminho(self):
        return self.caminho


class Item(QWidget):
    def __init__(self, parent, func, titulo="", label="", icone="", ):
        super(Item, self).__init__(parent)
        self.salvo = True
        self.layout = QGridLayout(self)
        self.layout.setSpacing(0)
        self.func = func
        self.titulo = titulo
        self.label = label
        self.icone = icone
        self.label_titulo = QLabel(self.titulo)
        self.label_titulo.setFont(QFont('SansSerif', 15))
        self.label_descricao = QLabel(self.label)
        self.label_titulo.setStyleSheet("border:2px solid #404040; background:#404040;")
        self.label_descricao.setStyleSheet("border:2px solid #404040; background:#404040;")
        palavras = QVBoxLayout(self)
        self.layout.addLayout(palavras, 0, 0)
        palavras.addWidget(self.label_titulo)
        palavras.addWidget(self.label_descricao)

        self.setFixedHeight(100)

    def mousePressEvent(self, mouse_event):
        self.func()

    def enterEvent(self, event):
        self.label_titulo.setStyleSheet("border-top: 2px solid #5cb50d;background:#404040;")
        self.label_descricao.setStyleSheet("border-top: 2px solid #404040;background:#404040;")

    def leaveEvent(self, event):
        self.label_titulo.setStyleSheet("border:2px solid #404040;background:#404040;")
        self.label_descricao.setStyleSheet("border:2px solid #404040;background:#404040;")


class Mascote(QWidget):
    def __init__(self, parent):
        super(Mascote, self).__init__(parent)
