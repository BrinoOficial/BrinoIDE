#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import webbrowser

from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel, QSizePolicy, QVBoxLayout


class BoasVindas(QWidget):
    def __init__(self, parent):
        super(BoasVindas, self).__init__(parent)
        self.layout = QGridLayout(self)
        self.parent = parent
        self.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.setStyleSheet("background:#404040; color:#efefef; padding:5")
        self.layout.setColumnStretch(0, 1)
        # self.layout.setColumnStretch(1, 12)
        self.layout.setRowStretch(0, 1)
        self.layout.setRowStretch(1, 1)
        self.layout.setSpacing(10)
        self.setContentsMargins(0, 0, 0, 0)
        self.layout.addWidget(Mascote(self), 0, 0)
        self.setAutoFillBackground(True)
        self.itens = QVBoxLayout(self)
        self.popular_itens()

    def popular_itens(self):
        novo = Item(self, self.parent.nova_aba, "Rascunho em Branco", "Crie um novo rascunho do zero",
                    os.path.join('recursos', 'novoArquivo.png'))
        aprender_mais = Item(self, self.abrir_site, "Não sabe como começar?",
                             "Visite nosso site para ler um de nossos tutoriais!", "")
        self.layout.addLayout(self.itens, 0, 0)
        self.itens.addWidget(novo)
        self.itens.addWidget(aprender_mais)
        self.setFixedHeight(300)

    def abrir_site(self):
        webbrowser.open("http://brino.cc/tutoriais.php", 1, True)


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
        palavras = QVBoxLayout(self)
        self.layout.addLayout(palavras, 0, 0)
        palavras.addWidget(self.label_titulo)
        palavras.addWidget(self.label_descricao)

        self.setFixedHeight(100)

    def mousePressEvent(self, QMouseEvent):
        self.func()

    def enterEvent(self, QEvent):
        pass


class Mascote(QWidget):
    def __init__(self, parent):
        super(Mascote, self).__init__(parent)
