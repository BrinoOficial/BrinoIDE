

"""
Br.ino Qt editor de texto

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
    mas SEM QUALQUER GARANTIA sem a garantia implicita de
    COMERCIALIZACAO ou ADEQUACAO A UM DETERMINADO PROPOSITO.
    Consulte a Licenca Publica Geral GNU para obter mais detalhes.

    Voce deveria ter recebido uma copia da Licenca Publica Geral
    GNU junto com este programa. Caso contrario, veja
    <https://www.gnu.org/licenses/>

    Codigo fonte retirado de:
    https: http://doc.qt.io/qt-5/qtwidgets-widgets-codeeditor-example.html
    **  Copyright (C) 2016 The Qt Company Ltd.
    **
    **  "Redistribution and use in source and binary forms, with or without
    ** modification, are permitted provided that the following conditions are
    ** met:
    **   * Redistributions of source code must retain the above copyright
    **     notice, this list of conditions and the following disclaimer.
    **   * Redistributions in binary form must reproduce the above copyright
    **     notice, this list of conditions and the following disclaimer in
    **     the documentation and/or other materials provided with the
    **     distribution.
    **   * Neither the name of The Qt Company Ltd nor the names of its
    **     contributors may be used to endorse or promote products derived
    **     from this software without specific prior written permission.
    **
    **
    ** THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
    ** "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
    ** LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
    ** A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
    ** OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
    ** SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
    ** LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES LOSS OF USE,
    ** DATA, OR PROFITS OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
    ** THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
    ** (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
    ** OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE."

website: brino.cc
modificado por: Mateus Berardo
email: mateus.berardo@brino.cc
modificado por: Victor Rodrigues Pacheco
email: victor.pacheco@brino.cc
"""

import functools
import ntpath
import os

from PyQt5.QtCore import QRect, Qt, QSize
from PyQt5.QtGui import QColor, QTextFormat, QPainter
from PyQt5.QtWidgets import QPlainTextEdit, QTextEdit, QWidget, QInputDialog, QMessageBox

import Main


class CodeEditor(QPlainTextEdit):

    def __init__(self, parent, ask=True, path="", salvar_caminho=True):
        super(CodeEditor, self).__init__(parent)
        # Contador de linhas
        self.contador_de_linhas = ContadorDeLinhas(self)
        self.largura_contador = 38
        self.blockCountChanged.connect(self.atualizar_largura_contador)
        self.updateRequest.connect(self.atualizar_area_contador)
        self.cursorPositionChanged.connect(self.marcar_linha_atual)
        self.contador_de_linhas.setGeometry(QRect(0, 0, self.largura_contador, self.height()))
        self.setViewportMargins(self.largura_contador, 0, 0, 0)
        self.marcar_linha_atual()
        self.achar = Achar(self)
        self.caminho = ""
        self.textChanged.connect(functools.partial(self.set_salvo, False))
        # Dialogo para novo arquivo
        if ask:
            self.nome, ok = QInputDialog.getText(None, "Novo arquivo", "Nome do rascunho:")
            if ok and self.nome != "":
                self.caminho = os.path.join(Main.get_caminho_padrao(), self.nome, self.nome + ".brpp")
                with open(os.path.join('recursos', 'exemplos', 'CodigoMinimo.brpp')) as arquivo:
                    self.set_texto(arquivo.read())
            elif not ok:
                return
            else:
                QMessageBox().warning(None, 'Erro', "Favor insira um nome", QMessageBox.Ok)
        else:
            self.nome = "Novo"
        # TODO oq isso faz?
        if path and salvar_caminho:
            self.caminho = path
            head, tail = ntpath.split(path)
            self.nome = ntpath.basename(head)
            with open(self.caminho) as arquivo:
                self.set_texto(arquivo.read())
        elif path:
            with open(path) as arquivo:
                self.set_texto(arquivo.read())
        self.salvo = True

    def atualizar_largura_contador(self):
        """
        Atualiza a largura e a altura do contador
        :return: None
        """
        self.contador_de_linhas.setGeometry(QRect(0, 0, self.largura_contador, self.height()))

    def atualizar_area_contador(self, rect, dy):
        """
        Realiza o scroll do contador
        :param rect:
            Retangulo de conteudos
        :param dy:
            Variacao na posicao y
        :return:
            None
        """
        if dy != 0:
            self.contador_de_linhas.scroll(0, dy)
        else:
            self.contador_de_linhas.update(0, rect.y(), self.contador_de_linhas.width(), rect.height())

            if rect.contains(self.viewport().rect()):
                self.atualizar_largura_contador()

    def set_salvo(self, estado):
        """
        Variavel para informar quando o documento nao precisa ser salvo
        :param estado:
            Se o arquivo ja foi salvo ou nao
        :return:
            None
        """
        self.salvo = estado

    def marcar_linha_atual(self):
        """
        Da hightlight na linha do cursor
        :return:
            None
        """
        selecoes_extras = list()
        if not self.isReadOnly():
            selecao = QTextEdit.ExtraSelection()
            cor_linha = QColor("#505050")
            selecao.format.setBackground(cor_linha)
            selecao.format.setProperty(QTextFormat.FullWidthSelection, True)
            selecao.cursor = self.textCursor()
            selecao.cursor.clearSelection()
            selecoes_extras.append(selecao)
        self.setExtraSelections(selecoes_extras)

    def lineNumberAreaPaintEvent(self, QPaintEvent):
        """
        Pinta o contador de linhas
        :param QPaintEvent:
             evento
        :return:
            None
        """
        painter = QPainter(self.contador_de_linhas)
        painter.fillRect(QPaintEvent.rect(), QColor("#252525"))

        bloco = self.firstVisibleBlock()
        numero_bloco = bloco.blockNumber()
        top = int(self.blockBoundingGeometry(bloco).translated(self.contentOffset()).top())
        bottom = top + int(self.blockBoundingRect(bloco).height())
        painter.fillRect(self.contador_de_linhas.width() - 2, top, 1, self.contador_de_linhas.height(),
                         QColor("#505050"))

        while bloco.isValid() and top <= QPaintEvent.rect().bottom():
            if bloco.isVisible() and bottom >= QPaintEvent.rect().top():
                number = str(numero_bloco + 1)
                painter.setPen(QColor("#505050"))
                painter.drawText(0, top, self.contador_de_linhas.width() - 2, self.fontMetrics().height(),
                                 Qt.AlignRight, number)
            bloco = bloco.next()
            top = bottom
            bottom = top + int(self.blockBoundingRect(bloco).height())
            numero_bloco += 1

    def AcharEventoDePintura(self, QPaintEvent):
        """
        Pinta da funcao achar
        :param QPaintEvent:
            Evento
        :return:
            None
        """
        painter = QPainter(self.achar)
        painter.fillRect(QPaintEvent.rect(), QColor("#252525"))

        top = int(self.top())
        painter.fillRect(0, top, self.width(), 2, QColor("#505050"))

    def set_texto(self, texto):
        """
        Coloca o texto no QPlainText
        :param texto:
            Texto a ser inserido
        :return:
            None
        """
        self.setPlainText(texto)

    def get_texto(self):
        """
        Pega o texto do QPlainText
        :return:
            None
        """
        return self.toPlainText()

    def get_nome(self):
        """
        Pega o nome
        :return:
            None
        """
        return self.nome

    def get_caminho(self):
        """
        Pega o caminho
        :return:
            None
        """
        return self.caminho

    def set_caminho(self, caminho):
        """
        Seta o caminho
        :param caminho:
            Caminho a ser setado
        :return:
            None
        """
        self.caminho = caminho


class ContadorDeLinhas(QWidget):

    def __init__(self, editor):
        super(ContadorDeLinhas, self).__init__(editor)
        self.editor_de_codigo = editor

    def sizeHint(self):
        """
        Tamanho do contador de linhas
        :return:
            Tamanho do contador
        """
        return QSize(self.editor_de_codigo.largura_contador, 0)

    def paintEvent(self, event):
        """
        paint do contador de linhas
        :param event:
            Evento
        :return:
            None
        """
        self.editor_de_codigo.lineNumberAreaPaintEvent(event)


class Achar(QWidget):
    def __init__(self, editor):
        super(Achar, self).__init__(editor)
        self.editor_de_codigo = editor

    def initUI(self):
        pass

    def sizeHint(self):
        """
        Seta o tamanho do widget do achar
        :return:
            Tamanho do widget
        """
        return QSize(0, 20)

    def paintEvent(self, QPaintEvent):
        """
        Chama o paint do evento de pintura
        :param QPaintEvent:
            Evento
        :return:
            None
        """
        self.editor_de_codigo.AcharEventoDePintura(QPaintEvent)
