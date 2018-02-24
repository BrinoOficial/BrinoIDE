#!/usr/bin/python
# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QWidget, QGridLayout, QPlainTextEdit, QLineEdit, QPushButton, QCheckBox


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
    return monitor_serial


class MonitorSerial(QWidget):
    def __init__(self, parent=None):
        super(MonitorSerial, self).__init__(parent)

        self.init_ui()

    def init_ui(self):
        self.setGeometry(650, 50, 400, 500)
        layout = QGridLayout(self)
        layout.setColumnStretch(0, 8)
        layout.setColumnStretch(1, 2)
        layout.setRowStretch(0, 1)
        layout.setRowStretch(1, 12)
        layout.setRowStretch(2, 1)
        self.setStyleSheet("background:#252525")
        self.setWindowTitle('Monitor Serial')

        linha_envio = QLineEdit(self)
        linha_envio.setStyleSheet("border-radius:3px;background:#101010;margin-bottom:2px;margin-right:2px;")

        log_monitor = QPlainTextEdit(self)
        log_monitor.setReadOnly(True)
        log_monitor.setStyleSheet("border-radius:3px;background:#101010;margin-bottom:2px;margin-right:2px;")

        btn_enviar = QPushButton("Enviar")
        btn_enviar.setObjectName("btn_enviar_tag")
        btn_enviar.setStyleSheet("""#btn_enviar_tag{border-radius:2px;color:#252525;background:#5cb50d;margin:2px;}
                                    #btn_enviar_tag:hover{border:1px solid #5cb50d;color:#5cb50d;background:#252525}""")

        rolagem_check = QCheckBox(self)
        rolagem_check.setText("Rolagem-automática")

        layout.addWidget(linha_envio, 0, 0)
        layout.addWidget(log_monitor, 1, 0, 1, 0)
        layout.addWidget(btn_enviar, 0, 1)
        layout.addWidget(rolagem_check, 2, 0)
