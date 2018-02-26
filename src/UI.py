#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Br.ino Qt UI

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

import ntpath
import os
from tempfile import mkdtemp

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QWidget, QGridLayout, QPlainTextEdit, QTabWidget, QActionGroup, QPushButton, QFileDialog,
                             QAction, QInputDialog)
from PyQt5.QtGui import QTextCursor

import DestaqueSintaxe
import EditorDeTexto
import Menu
import Preferencias
from Compiler import compilar_arduino_builder
from GerenciadorDeKeywords import traduzir
from Main import get_caminho_padrao
from PacoteAlvo import PacoteAlvo
from PlataformaAlvo import PlataformaAlvo


class Centro(QWidget):

    def __init__(self, parent=None):
        super(Centro, self).__init__()
        self.widget_abas = None
        self.menu = None
        self.parent = parent
        self.pacotes = dict()
        self.temp_build = mkdtemp('build')
        self.temp_cache = mkdtemp('cache')
        self.log = None
        self.init_ui()

    # noinspection PyUnresolvedReferences
    def init_ui(self):
        layout = QGridLayout(self)
        layout.setRowStretch(0, 7.5)
        layout.setRowStretch(1, 2.5)
        layout.setColumnMinimumWidth(0, 60)
        layout.setSpacing(5)
        layout.setContentsMargins(0, 0, 0, 0)

        self.menu = Menu.Menu(self)
        layout.addWidget(self.menu, 0, 0, 2, 2)

        btn = QPushButton(self)
        btn.clicked.connect(self.nova_aba)

        self.widget_abas = QTabWidget(self.parent)
        self.widget_abas.tabCloseRequested.connect(self.remover_aba)
        self.widget_abas.setTabsClosable(False)
        self.widget_abas.setCornerWidget(btn, Qt.TopRightCorner)
        layout.addWidget(self.widget_abas, 0, 1, 1, 2)

        self.log = QPlainTextEdit(self)
        self.log.setStyleSheet("border-radius:5px;background:#101010;margin-bottom:5px;margin-right:5px;")
        self.log.setReadOnly(True)
        layout.addWidget(self.log, 1, 1, 1, 2)

        self.init_pacotes()
        self.criar_menu_placas()

        self.show()

        self.nova_aba()
        self.nova_aba(os.path.join('.', 'recursos', 'exemplos', 'CodigoMinimo.brpp'), False)
        self.remover_aba(0)


    def init_pacotes(self):
        # TODO index contribuido
        self.carregar_hardware(os.path.join('builder', 'hardware'))
        # TODO carregar_hardware_contribuido
        # TODO carregar_hardware_rascunhos
        # TODO criar preferencias ferramentas

    def remover_aba(self, index):
        if self.widget_abas.count() > 1:
            if index is not int:
                self.widget_abas.removeTab(self.widget_abas.currentIndex())
            else:
                widget = self.widget_abas.widget(index)
                if widget is not None:
                    widget.deleteLater()
                self.widget_abas.removeTab(index)
        if self.widget_abas.count() == 1:
            self.widget_abas.setTabsClosable(False)

    def nova_aba(self, path="", salvar_caminho=True):
        if self.widget_abas.count() == 0 or path:
            editor = EditorDeTexto.CodeEditor(self.widget_abas, False, path=path, salvar_caminho=salvar_caminho)
        else:
            editor = EditorDeTexto.CodeEditor(self.widget_abas, True, path=path, salvar_caminho=salvar_caminho)
        if self.widget_abas.count() == 1:
            self.widget_abas.setTabsClosable(True)
        text = editor.get_nome()
        editor.setStyleSheet("background:#252525")
        highlight = DestaqueSintaxe.PythonHighlighter(editor.document())
        self.widget_abas.addTab(editor, text)
        if editor.get_nome() == "":
            self.remover_aba(self.widget_abas.count() - 1)
        else:
            self.widget_abas.setCurrentIndex(self.widget_abas.count() - 1)

    def abrir(self):
        dialogo = self.criar_dialogo_arquivo("Abrir arquivo", "Abrir")
        if dialogo.exec_() == QFileDialog.Accepted:
            caminho = dialogo.selectedFiles()[0]
            self.nova_aba(caminho)

    def salvar(self):
        editor = self.widget_abas.widget(self.widget_abas.currentIndex())
        caminho = editor.get_caminho()
        if caminho != "":
            if not os.path.exists(os.path.dirname(caminho)):
                try:
                    os.makedirs(os.path.dirname(caminho))
                except OSError as exc:  # Guard against race condition
                    if exc.errno != exc.errno.EEXIST:
                        raise
            with open(editor.get_caminho(), "w") as arquivo:
                arquivo.write(editor.get_texto())
        else:
            self.salvar_como()

    def salvar_como(self):
        dialogo = self.criar_dialogo_arquivo('Salvar arquivo', 'Salvar')
        if dialogo.exec_() == QFileDialog.Accepted:
            caminho = dialogo.selectedFiles()[0]
            if not ntpath.basename(caminho).__contains__(".brpp"):
                caminho = os.path.join(caminho, ntpath.basename(caminho) + ".brpp")
            editor = self.widget_abas.widget(self.widget_abas.currentIndex())
            self.widget_abas.setTabText(self.widget_abas.currentIndex(), ntpath.basename(caminho).replace(".brpp", ""))
            editor.set_caminho(caminho)
            self.salvar()

    def selecionar_texto(self, cursor, texto, indice_inicial, len):
        conteudo = self.widget_abas.widget(self.widget_abas.currentIndex()).toPlainText()
        indice_comeco = conteudo.find(texto, indice_inicial)
        cursor.setPosition(indice_comeco, QTextCursor.MoveAnchor)
        cursor.setPosition(indice_comeco + len, QTextCursor.KeepAnchor)
        return cursor


    def comentar_linha(self):
        editor = self.widget_abas.widget(self.widget_abas.currentIndex())
        cursor_atual = editor.textCursor()
        posicao = cursor_atual.position()
        linha = cursor_atual.blockNumber()
        bloco_atual = editor.document().findBlockByLineNumber(linha)
        cursor = QTextCursor(bloco_atual)
        editor.setTextCursor(cursor)
        texto = bloco_atual.text()
        if texto.strip().startswith("//"):
            cursor = self.selecionar_texto(cursor, '/', cursor.position(), 2)
            cursor.removeSelectedText()
            cursor.setPosition(posicao - 2)
            editor.setTextCursor(cursor)
        else:
            editor.insertPlainText('//')
            cursor.setPosition(posicao + 2)
            editor.setTextCursor(cursor)

    def achar(self):
        editor = self.widget_abas.widget(self.widget_abas.currentIndex())
        texto, ok = QInputDialog.getText(None, "Buscar", "Achar:")
        if ok and texto != "":
            cursor = editor.textCursor()
            cursor = self.selecionar_texto(cursor, texto, cursor.position(), len(texto))
            editor.setTextCursor(cursor)
        return

    def achar_e_substituir(self):
        editor = self.widget_abas.widget(self.widget_abas.currentIndex())
        subs = "haaaa"
        texto, ok = QInputDialog.getText(None, "Buscar", "Achar:")
        if ok and texto != "":
            cursor = editor.textCursor()
            cursor = self.selecionar_texto(cursor, texto, cursor.position(), len(texto))
            cursor.removeSelectedText()
            editor.setTextCursor(cursor)
            editor.insertPlainText(subs)
        return


    @staticmethod
    def criar_dialogo_arquivo(titulo, acao):
        dialogo = QFileDialog()
        dialogo.setWindowTitle(titulo)
        dialogo.setLabelText(QFileDialog.FileName, "Arquivo:")
        dialogo.setLabelText(QFileDialog.LookIn, "Buscar em:")
        dialogo.setLabelText(QFileDialog.FileType, "Tipo de arquivo:")
        dialogo.setLabelText(QFileDialog.Accept, acao)
        dialogo.setLabelText(QFileDialog.Reject, "Cancelar")
        dialogo.setNameFilters(["Rascunhos Br.ino (*.brpp)", "Rascunhos Arduino (*.ino)"])
        dialogo.selectNameFilter("Rascunhos Br.ino (*.brpp)")
        dialogo.setDirectory(get_caminho_padrao())
        return dialogo

    def abrir_serial(self):
        self.parent.abrir_serial()

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

    @staticmethod
    def carregar_pacote_alvo(pacote_alvo, pasta):
        pastas = os.listdir(pasta)
        if len(pastas) == 0:
            return
        for item in pastas:
            plataforma_alvo = PlataformaAlvo(item, os.path.join(pasta, item), pacote_alvo)
            pacote_alvo.get_plataformas()[item] = plataforma_alvo

    def criar_menu_placas(self):
        placas = QActionGroup(self.parent)
        placas.setExclusive(True)
        for pacote_alvo in self.pacotes.values():
            for plataforma_alvo in pacote_alvo.get_lista_plataformas():
                nome = plataforma_alvo.get_preferencias().get("name")
                self.parent.menu_placas.addAction(QAction(nome, self))
                for placa in plataforma_alvo.get_placas().values():
                    if not placa.get_preferencias().get('hide'):
                        self.parent.menu_placas.addAction(placa.criar_acao(self))

    def on_troca_placa_ou_porta(self):
        plataforma = self.get_plataforma_alvo()
        pastas_bibliotecas = list()
        # if plataforma:
        #    core = self.get_preferencias_placa()
        pasta_plataforma = plataforma.get_pasta()
        pastas_bibliotecas.append(os.path.join(pasta_plataforma, 'libraries'))
        pastas_bibliotecas.append(os.path.join(get_caminho_padrao(), 'bibliotecas'))

    def get_preferencias_placa(self):
        placa_alvo = self.get_placa_alvo()
        if placa_alvo is None:
            return None
        nome_placa = placa_alvo.get_id()
        prefs = placa_alvo.get_preferencias()
        # TODO lidar com nome extendido
        # TODO lidar com ferramentas extras

        return prefs

    def get_placa_alvo(self):
        plataforma_alvo = self.get_plataforma_alvo()
        if plataforma_alvo:
            placa = Preferencias.get('board')
            return plataforma_alvo.get_placa(placa)

    def get_plataforma_alvo(self, pacote=None, plataforma=None):
        if pacote is None:
            pacote = Preferencias.get('target_package')
        if plataforma is None:
            plataforma = Preferencias.get('target_platform')
        p = self.pacotes.get(pacote)
        plataforma_alvo = p.get(plataforma)
        return plataforma_alvo

    def compilar(self):
        self.salvar()
        self.log.clear()
        placa_alvo = self.get_placa_alvo()
        plataforma_alvo = placa_alvo.get_plataforma()
        pacote_alvo = plataforma_alvo.get_pacote()
        editor = self.widget_abas.widget(self.widget_abas.currentIndex())
        caminho = editor.get_caminho()
        traduzir(caminho)
        resultado = compilar_arduino_builder(caminho, placa_alvo, plataforma_alvo, pacote_alvo, self.temp_build,
                                             self.temp_cache)
        self.log.insertPlainText(resultado)
