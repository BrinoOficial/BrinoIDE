from PyQt5.QtCore import QSize, QEvent
from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QAbstractButton

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
    
    Codigo fonte retirado de:
    https://stackoverflow.com/questions/44453268/creating-custom-pyqt5-image-button
    Autor: Atrum

website: brino.cc
modificado por: Mateus Berardo
email: mateus.berardo@brino.cc
modificado por: Victor Rodrigues Pacheco
email: victor.pacheco@brino.cc
"""


class botaoImagem(QAbstractButton):
    def __init__(self, pixmap, hover_pixmap, parent=None):
        super(botaoImagem, self).__init__(parent)
        self.pixmap = pixmap
        self.hover_pixmap = hover_pixmap
        self.installEventFilter(self)
        self.estado_botao = False

    def paintEvent(self, event):
        painter = QPainter(self)
        if self.estado_botao == False:
            painter.drawPixmap(event.rect(), self.pixmap)
        if self.estado_botao == True:
            painter.drawPixmap(event.rect(), self.hover_pixmap)

    def sizeHint(self):
        return QSize(50, 63)

    def enterEvent(self, QEvent):
        self.estado_botao = True
        self.update()

    def leaveEvent(self, QEvent):
        self.estado_botao = False
        self.update()

    def eventFilter(self, object, event):
        if event.type() == QAbstractButton.enterEvent:
            print "Hovering"
            return True
        if event.type() == QAbstractButton.leaveEvent:
            print "UnHovering"
            pass

        return False
