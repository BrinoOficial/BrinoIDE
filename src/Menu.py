#!/usr/bin/python
# -*- coding: utf-8 -*-

import os

from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QSpacerItem, QSizePolicy

from BotaoImagem import botaoImagem

"""
Br.ino Qt UI

Interface base da IDE Br.ino
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


class Menu(QWidget):

    def __init__(self):
        super(Menu, self).__init__()
        self.layout = 0

        self.init_ui()

    def init_ui(self):
        container = QWidget(self)
        container.setFixedWidth(60)
        layout = QVBoxLayout(container)
        container.setStyleSheet("background-color: '#5cb50d';")

        btn_compilar = botaoImagem(QPixmap(os.path.join('recursos', 'compilarFoco.png')), self)
        btn_compilar_e_carregar = botaoImagem(QPixmap(os.path.join('recursos', 'carregarFoco.png')), self)
        btn_novo = botaoImagem(QPixmap(os.path.join('recursos', 'novoArquivoFoco.png')), self)
        btn_abrir = botaoImagem(QPixmap(os.path.join('recursos', 'abrirPastaFoco.png')), self)
        btn_salvar = botaoImagem(QPixmap(os.path.join('recursos', 'salvarFoco.png')), self)
        btn_monitor_serial = botaoImagem(QPixmap(os.path.join('recursos', 'monitorSerialFoco.png')), self)
        btn_monitor_serial.setFixedSize(50, 50)

        layout.setContentsMargins(5, 5, 5, 0)
        espacador_vertical = QSpacerItem(0, 500000000, QSizePolicy.Minimum, QSizePolicy.Expanding)
        layout.addWidget(btn_compilar)
        layout.addWidget(btn_compilar_e_carregar)
        layout.addWidget(btn_novo)
        layout.addWidget(btn_abrir)
        layout.addWidget(btn_salvar)
        layout.addWidget(btn_monitor_serial)
        layout.addItem(espacador_vertical)

        self.show()
