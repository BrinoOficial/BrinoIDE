#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Br.ino Qt Menu

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

import os

from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QSpacerItem, QSizePolicy

from BotaoImagem import botaoImagem
from PacoteAlvo import PacoteAlvo
from PlataformaAlvo import PlataformaAlvo


class Menu(QWidget):

    def __init__(self, parent=None):
        super(Menu, self).__init__()
        self.layout = 0
        self.pacotes = dict()
        self.parent = parent
        self.init_ui()

    def init_ui(self):
        menu = QWidget(self)
        layout = QVBoxLayout(menu)
        menu.setStyleSheet("background-color: '#5cb50d';")

        btn_compilar = botaoImagem(QPixmap(os.path.join('recursos', 'compilar.png')),
                                   QPixmap(os.path.join('recursos', 'compilarFoco.png')), self)

        btn_compilar_e_carregar = botaoImagem(QPixmap(os.path.join('recursos', 'carregar.png')),
                                              QPixmap(os.path.join('recursos', 'carregarFoco.png')), self)
        btn_compilar_e_carregar.setFixedSize(50, 70)

        btn_novo = botaoImagem(QPixmap(os.path.join('recursos', 'novoArquivo.png')),
                               QPixmap(os.path.join('recursos', 'novoArquivoFoco.png')), self)
        btn_novo.clicked.connect(self.parent.nova_aba)

        btn_abrir = botaoImagem(QPixmap(os.path.join('recursos', 'abrirPasta.png')),
                                QPixmap(os.path.join('recursos', 'abrirPastaFoco.png')), self)
        btn_abrir.clicked.connect(self.parent.abrir)

        btn_salvar = botaoImagem(QPixmap(os.path.join('recursos', 'salvar.png')),
                                 QPixmap(os.path.join('recursos', 'salvarFoco.png')), self)
        btn_salvar.clicked.connect(self.parent.salvar)

        btn_monitor_serial = botaoImagem(QPixmap(os.path.join('recursos', 'monitorSerial.png')),
                                         QPixmap(os.path.join('recursos', 'monitorSerialFoco.png')), self)
        btn_monitor_serial.setFixedSize(50, 50)

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

    def carregar_hardware(self, pasta):
        if not os.path.isdir(pasta):
            return
        lista = [os.path.join(pasta, pasta_) for pasta_ in os.listdir(pasta) if
                 os.path.isdir(os.path.join(pasta, pasta_))]
        if len(lista) == 0:
            return
        lista = sorted(lista, key=str.lower)
        lista.remove(os.path.join(pasta, "tools"))
        for item in lista:
            nome_item = os.path.basename(item)
            if nome_item in self.pacotes:
                pacote_alvo = self.pacotes.get(nome_item)
            else:
                pacote_alvo = PacoteAlvo(nome_item)
                self.pacotes[nome_item] = pacote_alvo
            self.carregar_pacote_alvo(pacote_alvo, item)

    def carregar_pacote_alvo(self, pacote_alvo, pasta):
        pastas = os.listdir(pasta)
        if len(pastas) == 0:
            return
        for item in pastas:
            plataforma_alvo = PlataformaAlvo(item, os.path.join(pasta, item), pacote_alvo)
            pacote_alvo.get_plataformas()[item] = plataforma_alvo
