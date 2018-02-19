#!/usr/bin/python
# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QTextEdit, QWidget, QVBoxLayout


"""
Br.ino Qt monitor serial

Codigo do monitor serial da IDE Br.ino
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

def monitor_serial():
    print "Abrindo serial"
    monitor_serial = MonitorSerial()
    monitor_serial.show()


class MonitorSerial(QWidget):
    def __init__(self, parent=None):
        super(MonitorSerial, self).__init__(parent)

        self.init_ui()

    def init_ui(self):
        textEdit = QTextEdit()
        layout = QVBoxLayout()
        self.setLayout(layout)
        layout.addWidget(textEdit)
        self.setGeometry(300, 300, 250, 150)
        self.setWindowTitle('Quit button')
        self.show()
