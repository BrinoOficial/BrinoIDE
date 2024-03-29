#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Br.ino Qt Menu

Interface base da IDE Br.ino
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

website: brino.cc
author: Mateus Berardo
email: mateus.berardo@brino.cc
author: Victor Rodrigues Pacheco
email: victor.pacheco@brino.cc
"""

import os

from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QSpacerItem, QSizePolicy

from BotaoImagem import BotaoImagem


class Menu(QWidget):
    '''
    Classe responsavel pela barra verde de menu lateral. Nela temos as opcoes de compilar, compilar e carregar, novo,
     abrir, salvar e monitor serial
    '''

    def __init__(self, parent=None):
        super(Menu, self).__init__()
        self.layout = 0
        self.parent = parent
        self.init_ui()

    def init_ui(self):
        menu = QWidget(self)
        layout = QVBoxLayout(menu)
        menu.setStyleSheet("background-color: '#5cb50d';")

        # Adiciona os botoes e suas acoes ao menu lateral

        btn_compilar = BotaoImagem(QPixmap(os.path.join('recursos', 'compilar.png')),
                                   QPixmap(os.path.join('recursos', 'compilarFoco.png')), self)
        btn_compilar.clicked.connect(self.parent.compilar)
        btn_compilar.setStatusTip("Compilar código")

        btn_compilar_e_carregar = BotaoImagem(QPixmap(os.path.join('recursos', 'carregar.png')),
                                              QPixmap(os.path.join('recursos', 'carregarFoco.png')), self)
        btn_compilar_e_carregar.setFixedSize(50, 70)
        btn_compilar_e_carregar.clicked.connect(self.parent.parent.enviar_codigo)
        btn_compilar_e_carregar.setStatusTip("Compilar e carregar código")

        btn_novo = BotaoImagem(QPixmap(os.path.join('recursos', 'novoArquivo.png')),
                               QPixmap(os.path.join('recursos', 'novoArquivoFoco.png')), self)
        btn_novo.clicked.connect(self.parent.nova_aba)
        btn_novo.setStatusTip("Criar novo arquivo Brino")

        btn_abrir = BotaoImagem(QPixmap(os.path.join('recursos', 'abrirPasta.png')),
                                QPixmap(os.path.join('recursos', 'abrirPastaFoco.png')), self)
        btn_abrir.clicked.connect(self.parent.abrir)
        btn_abrir.setStatusTip("Abrir arquivo")

        btn_salvar = BotaoImagem(QPixmap(os.path.join('recursos', 'salvar.png')),
                                 QPixmap(os.path.join('recursos', 'salvarFoco.png')), self)
        btn_salvar.clicked.connect(self.parent.salvar)
        btn_salvar.setStatusTip("Salvar arquivo")

        btn_monitor_serial = BotaoImagem(QPixmap(os.path.join('recursos', 'monitorSerial.png')),
                                         QPixmap(os.path.join('recursos', 'monitorSerialFoco.png')), self)
        btn_monitor_serial.setFixedSize(50, 50)
        btn_monitor_serial.clicked.connect(self.parent.parent.abrir_serial)
        btn_monitor_serial.setStatusTip("Abrir monitor serial")

        # Layout do menu
        espacador_vertical = QSpacerItem(0, 50000, QSizePolicy.Expanding, QSizePolicy.Expanding)

        layout.setContentsMargins(5, 5, 5, 5)
        layout.addWidget(btn_compilar)
        layout.addWidget(btn_compilar_e_carregar)
        layout.addWidget(btn_novo)
        layout.addWidget(btn_abrir)
        layout.addWidget(btn_salvar)
        layout.addWidget(btn_monitor_serial)
        layout.addItem(espacador_vertical)
        self.show()
