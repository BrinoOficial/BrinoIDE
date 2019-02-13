#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Br.ino Qt botoes com animacao do menu

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
    
    Codigo fonte retirado de:
    https://stackoverflow.com/questions/44453268/creating-custom-pyqt5-image-button
    Autor: Atrum

website: brino.cc
modificado por: Mateus Berardo
email: mateus.berardo@brino.cc
modificado por: Victor Rodrigues Pacheco
email: victor.pacheco@brino.cc
"""

from PyQt5.QtCore import QSize
from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QAbstractButton


class BotaoImagem(QAbstractButton):
    def __init__(self, pixmap, hover_pixmap, parent=None):
        super(BotaoImagem, self).__init__(parent)
        self.pixmap = pixmap
        self.hover_pixmap = hover_pixmap
        self.installEventFilter(self)
        self.estado_botao = False

    def paintEvent(self, event):
        painter = QPainter(self)
        if not self.estado_botao:
            painter.drawPixmap(event.rect(), self.pixmap)
        else:
            painter.drawPixmap(event.rect(), self.hover_pixmap)

    def sizeHint(self):
        """
        Define o tamanho dos botoes
        :return:
            Tamanho dos botoes
        """
        return QSize(50, 63)

    def enterEvent(self, QEvent):
        """
        Evento de entrada do botao
        :param QEvent:
            Evento
        :return:
            None
        """
        self.estado_botao = True
        self.update()

    def leaveEvent(self, QEvent):
        """
        Evento de saida do botao
        :param QEvent:
            Evento
        :return:
            None
        """
        self.estado_botao = False
        self.update()
