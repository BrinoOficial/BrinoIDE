#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Br.ino Qt editor de texto

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

auto-complete modificado a partir do codigo de smitkpatel
disponivel em https://stackoverflow.com/questions/28956693/pyqt5-qtextedit-auto-completion
"""

import ntpath
import os

import functools
import re
from PyQt5.QtCore import QRect, Qt, QSize
from PyQt5.QtGui import QColor, QTextFormat, QPainter, QTextCursor
from PyQt5.QtWidgets import QPlainTextEdit, QCompleter, QTextEdit, QWidget, QInputDialog, QMessageBox

import DestaqueSintaxe
import Main
import MeuDicionarioComplete


class CodeEditor(QPlainTextEdit):

    def __init__(self, parent, ask=True, path="", salvar_caminho=True):
        super(CodeEditor, self).__init__(parent)
        # Contador de linhas
        self.highlight = None
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
            valido = False
            while not valido:
                self.nome, ok = QInputDialog.getText(None, "Novo arquivo", "Nome do rascunho:")
                if ok:
                    if CodeEditor.validar(self.nome):
                        self.caminho = os.path.join(Main.get_caminho_padrao(), self.nome, self.nome + ".brpp")
                        if os.path.exists(self.caminho):
                            arq_existe = QMessageBox().warning(None, 'Arquivo existe',
                                                               "Ao abrir esse arquivo, você apagará um arquivo "+
                                                               "existente. Gostaria de continuar?",
                                                               QMessageBox.Ok | QMessageBox.No)
                            if arq_existe == QMessageBox.Ok:
                                with open(os.path.join('recursos', 'exemplos', 'CodigoMinimo.brpp')) as arquivo:
                                    self.set_texto(arquivo.read())
                                valido = True
                            else:
                                valido = False
                        else:
                            with open(os.path.join('recursos', 'exemplos', 'CodigoMinimo.brpp')) as arquivo:
                                self.set_texto(arquivo.read())
                            valido = True
                    else:
                        QMessageBox().warning(None, 'Erro', "Nome inválido!", QMessageBox.Ok)
                        valido = False
                else:
                    return
        else:
            self.nome = "Novo"
        if path:
            if salvar_caminho:
                self.caminho = path
                diretorio, nome = ntpath.split(path)
                self.nome = ntpath.basename(diretorio)
            with open(path) as arquivo:
                self.set_texto(arquivo.read())
        self.salvo = True
        self.highlight = DestaqueSintaxe.PythonHighlighter(self.document())
        self.completer = MeuDicionarioComplete.MeuDicionarioComplete()
        self.completer.popup().setStyleSheet("""
            background: #101010;
            color: #efefef;
        """)
        self.setCompleter(self.completer)

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

    @staticmethod
    def validar(nome):
        regex = re.compile('[A-Za-z_-]+[0-9A-Za-z_-]*')
        return re.match(regex, nome)

    def setCompleter(self, completer):
        #        if self.completer:
        #            self.disconnect(self.completer, 0, self, 0)
        #        if not completer:
        #            return
        completer.setWidget(self)
        completer.setCompletionMode(QCompleter.PopupCompletion)
        completer.setCaseSensitivity(Qt.CaseSensitive)
        self.completer = completer
        self.completer.insertText.connect(self.insertCompletion)

    def insertCompletion(self, completion):
        tc = self.textCursor()
        extra = (len(completion) -
                 len(self.completer.completionPrefix()))
        tc.movePosition(QTextCursor.Left)
        tc.movePosition(QTextCursor.EndOfWord)
        tc.insertText(completion[-extra:])
        self.setTextCursor(tc)

    def textUnderCursor(self):
        tc = self.textCursor()
        tc.select(QTextCursor.WordUnderCursor)
        return tc.selectedText()

    def focusInEvent(self, event):
        if self.completer:
            self.completer.setWidget(self)
        QPlainTextEdit.focusInEvent(self, event)

    def keyPressEvent(self, event):
        if self.completer and self.completer.popup() and self.completer.popup().isVisible():
            if event.key() in (
                    Qt.Key_Enter,
                    Qt.Key_Return,
                    Qt.Key_Escape,
                    Qt.Key_Backtab):
                event.ignore()
                return
        # ctrl+espaco foi pressionado?
        e_atalho = (event.modifiers() == Qt.ControlModifier and event.key() == Qt.Key_Space)
        # modifier to complete suggestion inline ctrl-e
        inline = (event.modifiers() == Qt.ControlModifier and event.key() == Qt.Key_E) or (
                self.completer.popup().isVisible() and event.key() == Qt.Key_Tab)
        # if inline completion has been chosen
        if inline:
            # set completion mode as inline
            self.completer.setCompletionMode(QCompleter.InlineCompletion)
            prefixo_a_completar = self.textUnderCursor()
            if (prefixo_a_completar != self.completer.completionPrefix()):
                self.completer.setCompletionPrefix(prefixo_a_completar)
            self.completer.complete()
            #            self.completer.setCurrentRow(0)
            #            self.completer.activated.emit(self.completer.currentCompletion())
            # set the current suggestion in the text box
            self.completer.insertText.emit(self.completer.currentCompletion())
            # reset the completion mode
            self.completer.setCompletionMode(QCompleter.PopupCompletion)
            return
        if (not self.completer or not e_atalho):
            pass
            QPlainTextEdit.keyPressEvent(self, event)
        # debug
        #        print("After controlspace")
        #        print("e_atalho is: {}".format(e_atalho))
        # debug over
        # ctrl or shift key on it's own??
        ctrlOrShift = event.modifiers() in (Qt.ControlModifier, Qt.ShiftModifier)
        if ctrlOrShift and event.text() == '':
            #             ctrl or shift key on it's own
            return
        # debug
        #        print("After on its own")
        #        print("e_atalho is: {}".format(e_atalho))
        # debug over
        #        eow = "~!@#$%^&*()_+{}|:\"<>?,./;'[]\\-=" #fim da palavra
        eow = "~!@#$%^&*+{}|:\"<>?,./;'[]\\-="  # fim da palavra

        hasModifier = ((event.modifiers() != Qt.NoModifier) and not ctrlOrShift)

        prefixo_a_completar = self.textUnderCursor()
        #         print('event . text = {}'.format(event.text().right(1)))
        #         if (not e_atalho and (hasModifier or event.text()=='' or\
        #                                 len(prefixo_a_completar) < 3 or \
        #                                 eow.contains(event.text().right(1)))):
        if not e_atalho:
            if self.completer.popup():
                self.completer.popup().hide()
            return
        #        print("complPref: {}".format(prefixo_a_completar))
        #        print("completer.complPref: {}".format(self.completer.prefixo_a_completar()))
        #        print("mode: {}".format(self.completer.completionMode()))
        #        if (prefixo_a_completar != self.completer.prefixo_a_completar()):
        self.completer.setCompletionPrefix(prefixo_a_completar)
        popup = self.completer.popup()
        popup.setCurrentIndex(
            self.completer.completionModel().index(0, 0))
        cr = self.cursorRect()
        cr.setWidth(self.completer.popup().sizeHintForColumn(0)
                    + self.completer.popup().verticalScrollBar().sizeHint().width())
        self.completer.complete(cr)  # popup it up!


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
