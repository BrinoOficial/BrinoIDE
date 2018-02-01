from PyQt4 import QtGui

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

author: Mateus Berardo
website: brino.cc
email: mateus.berardo@brino.cc
"""


class Centro(QtGui.QWidget):

    def __init__(self):
        super(Centro, self).__init__()
        self.layout = 0

        self.init_ui()

    def init_ui(self):
        layout = QtGui.QGridLayout(self)
        menu = QtGui.QWidget(self)
        menu.setStyleSheet("background: '#5cb50d';")
        layout.addWidget(menu, 0, 0)
        layout.setMargin(0)
        editor = QtGui.QTextEdit(self)
        layout.addWidget(editor, 0, 1, 0, 7)

        self.show()
