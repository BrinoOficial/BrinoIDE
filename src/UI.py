#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Br.ino Qt UI

Interface base da IDE Br.ino
em PyQt5 (python 3.6)

    IDE do Br.ino  Copyright (C) 2018  Br.ino

    Este arquivo e parte da IDE do Br.ino.

    A IDE do Br.ino eh um software livre: voce pode redistribui-lo
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

website: https://brino.cc
github: https://github.com/BrinoOficial/BrinoIDE
author: Mateus Berardo
author: Victor Rodrigues Pacheco
author: Gabriel Rodrigues Pacheco
"""

import glob
import ntpath
import os
import sys
from tempfile import mkdtemp
from google_measurement_protocol import event, report
import functools
import serial
import shutil

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QTextCursor
from PyQt5.QtWidgets import (QWidget, QGridLayout, QPlainTextEdit, QTabWidget, QActionGroup, QPushButton, QFileDialog,
                             QAction, QInputDialog, QMessageBox, QMenu)

import EditorDeTexto
import Main
import Menu
import Preferencias
import Uploader
import Rastreador
from BoasVindas import BoasVindas
from Compiler import *
from GerenciadorDeKeywords import traduzir
from IndexadorContribuicao import IndexadorContribuicao
from Main import get_caminho_padrao
from PacoteAlvo import PacoteAlvo
from PlataformaAlvo import PlataformaAlvo

import os
import sys
import webbrowser
from urllib.request import urlopen
import uuid
import requests
import traceback
import re

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QSplashScreen, QMainWindow, QApplication, QAction, QMenu, QStatusBar, QMessageBox, QLabel

import GerenciadorDeCodigo
import GerenciadorDeLinguas
import MonitorSerial
import Preferencias
import UI
from exceptions import UpdateException
import Rastreador

# TODO Duplicado, resolver isso
versao = '3.0.7'
caminho_padrao = ''
s = 3

class Centro(QWidget):

    def __init__(self, parent=None):
        super(Centro, self).__init__()
        self.widget_abas = None
        self.menu = None
        self.indexer = None
        self.parent = parent
        self.pacotes = dict()
        # TODO Remover arquivos temporarios
        self.temp_build = mkdtemp('build')
        self.temp_cache = mkdtemp('cache')
        self.log = None
        self.init_ui()

    # noinspection PyUnresolvedReferences
    def init_ui(self):
        # Define grid
        layout = QGridLayout(self)
        layout.setRowStretch(0, 7)
        layout.setRowStretch(1, 2)
        layout.setColumnMinimumWidth(0, 60)
        layout.setSpacing(5)
        layout.setContentsMargins(0, 0, 0, 0)

        # Cria menu
        self.menu = Menu.Menu(self)
        layout.addWidget(self.menu, 0, 0, 2, 2)

        # Botao para criar nova aba
        btn = QPushButton(self)
        btn.clicked.connect(self.nova_aba)
        btn.setStatusTip("Abrir nova aba")

        # Cria o widget abas
        self.widget_abas = QTabWidget(self.parent)
        self.widget_abas.tabCloseRequested.connect(self.remover_aba)
        self.widget_abas.setTabsClosable(False)
        self.widget_abas.setCornerWidget(btn, Qt.TopRightCorner)
        self.widget_abas.setStyleSheet("background:#252525;")
        layout.addWidget(self.widget_abas, 0, 1, 1, 2)

        # Cria log
        self.log = QPlainTextEdit(self)
        self.log.setStyleSheet("border-radius:5px;background:#101010;margin-bottom:5px;margin-right:5px;")
        self.log.setReadOnly(True)
        self.log.setStatusTip("Log")
        layout.addWidget(self.log, 1, 1, 1, 2)

        # Carrega pacotes de hardware
        self.init_pacotes()
        # Cria menu de placas
        self.criar_menu_placas()
        self.criar_menu_exemplos()

        # Adiciona a aba de boas vindas
        self.widget_abas.addTab(BoasVindas(self), "Bem-Vindo")
        self.show()
        Rastreador.log_info("WidgetCentral Carregado")

    def init_pacotes(self):
        """
        Carrega os pacotes de hardware do Arduino
        :return:
            None
        """
        pasta_hardware = os.path.join('builder', 'hardware')
        self.indexer = IndexadorContribuicao(os.path.join('builder'), pasta_hardware)
        self.indexer.parse_index()
        self.indexer.sincronizar_com_arquivos()
        self.carregar_hardware(pasta_hardware)
        self.carregar_hardware_contribuido(self.indexer)
        self.carregar_hardware(os.path.join(Main.get_caminho_padrao(), 'hardware'))
        Rastreador.log_info("Pacotes de hardware carregados")

    def remover_aba(self, index, fechando=False):
        """
        Remove a aba
        :param index:
            Indice da aba
        :param fechando:
            Indica se o programa esta fechando
            default: False
        :return:
            None
        """
        Rastreador.log_debug("Removendo uma aba")
        if self.widget_abas.count() > 1 or fechando:
            # Se o index for argumento padrao do sinal (QT)
            if type(index) is not int:
                self.remover_aba(self.widget_abas.currentIndex())
            else:
                arquivo = self.widget_abas.widget(index)
                self.widget_abas.setCurrentIndex(index)
                if not arquivo.salvo:
                    ret = QMessageBox(self)
                    ret.setText("Gostaria de salvar este código antes de sair?")
                    ret.setIcon(QMessageBox.Question)
                    ret.addButton("Não Salvar", QMessageBox.NoRole)
                    ret.addButton("Cancelar", QMessageBox.RejectRole)
                    ret.addButton("Salvar", QMessageBox.AcceptRole)
                    ret = ret.exec_()
                    if ret == 1:
                        return False
                    elif ret == 2:
                        self.salvar()
                if arquivo is not None:
                    arquivo.deleteLater()
                self.widget_abas.removeTab(index)
        if self.widget_abas.count() == 1:
            self.widget_abas.setTabsClosable(False)

        return True

    def nova_aba(self, path="", salvar_caminho=True):
        """
        Criar nova aba de editor de texto
        :param path:
            Caminho para o arquivo a ser aberto
        :param salvar_caminho:
            Se o caminho deve ser definido como local para salvar
        :return:
            None
        """
        Rastreador.log_debug("Criando nova aba")
        if self.widget_abas.count() == 0 or path:
            editor = EditorDeTexto.CodeEditor(self.widget_abas, False, path=path, salvar_caminho=salvar_caminho)
        else:
            editor = EditorDeTexto.CodeEditor(self.widget_abas, True, path=path, salvar_caminho=salvar_caminho)
        if self.widget_abas.count() == 1:
            self.widget_abas.setTabsClosable(True)
        identificador_aba = editor.get_nome()
        if len(identificador_aba) > 10:
            identificador_aba = identificador_aba[:10] + "..."
        editor.setStyleSheet("background:#252525")
        # Adiciona a aba se o arquivo tiver nome
        if editor.get_nome():
            self.widget_abas.addTab(editor, identificador_aba)
            Rastreador.log_info("Aberta aba %s"%editor.get_nome())
        if editor.get_nome() == "":
            self.remover_aba(self.widget_abas.count() - 1)
        else:
            self.widget_abas.setCurrentIndex(self.widget_abas.count() - 1)
        # Define que nao eh necessario salvar pois acabou de ser aberto
        editor.set_salvo(True)

    def abrir_traducao(self):
        """
        Abrir a traducao auto gerada em uma nova aba

        :return:
            None
        """
        Rastreador.log_debug("Abrindo tradução")
        self.salvar()

        editor = self.widget_abas.widget(self.widget_abas.currentIndex())
        caminho_traducao = editor.get_caminho()
        if caminho_traducao == 0 or caminho_traducao == "":
            Rastreador.log_error("Erro ao carregar caminho da tradução. Caminho é "+str(caminho_traducao))
            return
        traduzir(caminho_traducao)
        caminho_traducao = caminho_traducao.replace("brpp", "ino")
        Rastreador.log_debug("Tradução carregada, abrindo tradução")
        self.abrir(caminho=caminho_traducao, exemplo=True)

    def abrir(self, caminho=None, exemplo=True):
        """
        Abrir arquivo .ino ou .brpp em nova aba
        :param caminho:
            endereço para abrir
        :param exemplo:
            indicacao se o arquivo pode ser sobrescrito
        :return:
            None
        """
        Rastreador.log_debug("Abrindo arquivo")
        if caminho is None or not caminho:
            salvar_caminho = True
            dialogo = self.criar_dialogo_arquivo("Abrir arquivo", "Abrir")
            if dialogo.exec_() == QFileDialog.Accepted:
                caminho = dialogo.selectedFiles()[0]
                # Testa se o arquivo existe
                if os.path.exists(caminho):
                    self.nova_aba(caminho, salvar_caminho)
                else:
                    QMessageBox(QMessageBox.Warning, "Erro", "O arquivo não existe", QMessageBox.NoButton, self).show()
                    Rastreador.log_error("Arquivo inexistente")
        else:
            if not os.path.exists(caminho):
                Rastreador.log_error("Arquivo não existe")
                return
            self.nova_aba(caminho)
            widget = self.widget_abas.widget(self.widget_abas.currentIndex())
            if exemplo:
                widget.caminho = ""

    def salvar(self):
        """
        Salvar arquivo da aba atual
        :return:
            None
        """
        editor = self.widget_abas.widget(self.widget_abas.currentIndex())
        caminho = editor.get_caminho()
        # Testa se a aba eh a de boas vindas
        if caminho == 0:
            return
        # Testa se a aba eh a de boas vindas
        editor.set_salvo(True)
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
        """
        Salvar arquivo atual como
        :return:
            None
        """
        editor = self.widget_abas.widget(self.widget_abas.currentIndex())
        caminho = editor.get_caminho()
        # Testa se a aba eh a de boas vindas
        if caminho == 0:
            return
        caminho = editor.get_caminho()
        dialogo = self.criar_dialogo_arquivo('Salvar arquivo', 'Salvar')
        if dialogo.exec_() == QFileDialog.Accepted:
            caminho = dialogo.selectedFiles()[0]
            # Verifica se a pessoa selecionou a pasta ao inves do arquivo em si
            if not ntpath.basename(caminho).__contains__(".brpp"):
                caminho = os.path.join(caminho, ntpath.basename(caminho) + ".brpp")
            # Troca o identificador da aba
            identificador_aba = ntpath.basename(caminho).replace(".brpp", "")
            if len(identificador_aba) > 10:
                identificador_aba = identificador_aba[:10] + "..."
            self.widget_abas.setTabText(self.widget_abas.currentIndex(), identificador_aba)
            editor.set_caminho(caminho)
            self.salvar()

    def selecionar_texto(self, cursor, texto, indice_inicial, comprimento):
        """
        Seleciona texto
        :param cursor:
            Cursor do documento
        :param texto:
            Texto a ser selecionado
        :param indice_inicial:
            Ponto de onde comecar a busca
        :param comprimento:
            Tamanho do texto
        :return cursor:
            Cursor com a selecao
        """
        conteudo = self.widget_abas.widget(self.widget_abas.currentIndex()).toPlainText()
        indice_comeco = conteudo.find(texto, indice_inicial)
        if indice_comeco == -1:
            indice_comeco = conteudo.find(texto, 0)
        if not indice_comeco == -1:
            cursor.setPosition(indice_comeco, QTextCursor.MoveAnchor)
            cursor.setPosition(indice_comeco + comprimento, QTextCursor.KeepAnchor)
            return cursor
        return -1

    def comentar_linha(self):
        """
        comenta a linha
        :return:
            None
        """
        editor = self.widget_abas.widget(self.widget_abas.currentIndex())
        caminho = editor.get_caminho()
        # Testa se a aba eh a de boas vindas
        if caminho == 0:
            return
        cursor_atual = editor.textCursor()
        posicao = cursor_atual.position()
        bloco_atual = cursor_atual.block()
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
        """
        Achar palavra chave no codigo
        :return:
            None
        """
        editor = self.widget_abas.widget(self.widget_abas.currentIndex())
        caminho = editor.get_caminho()
        # Testa se a aba eh a de boas vindas
        if caminho == 0:
            return
        texto, ok = QInputDialog.getText(None, "Buscar", "Achar:")
        if ok and texto != "":
            cursor = editor.textCursor()
            cursor = self.selecionar_texto(cursor, texto, cursor.position(), len(texto))
            if not cursor == -1:
                editor.setTextCursor(cursor)

    def achar_e_substituir(self):
        """
        Achar e substituir palavras chave por outras
        :return:
            None
        """
        editor = self.widget_abas.widget(self.widget_abas.currentIndex())
        caminho = editor.get_caminho()
        # Testa se a aba eh a de boas vindas
        if caminho == 0:
            return
        texto, ok = QInputDialog.getText(None, "Achar", "Achar:")
        subs, ok = QInputDialog.getText(None, "Substituir", "Substituir:")
        if ok and texto != "":
            cursor = editor.textCursor()
            cursor = self.selecionar_texto(cursor, texto, cursor.position(), len(texto))
            if not cursor == -1:
                cursor.removeSelectedText()
                editor.setTextCursor(cursor)
                editor.insertPlainText(subs)
        return

    @staticmethod
    def criar_dialogo_arquivo(titulo, acao):
        """
        Cria dialogo personalizado para buscar arquivos
        :param titulo:
            Titulo de aba
        :param acao:
            Texto do botao de selecionar
        :return dialogo:
            dialogo
        """
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
        """
        Abre o monitor serial
        :return:
            None
        """
        self.parent.abrir_serial()

    def carregar_hardware(self, pasta):
        """
        Carrega as opcoes de hardware do Arduino
        :param pasta:
            Diretorio do hardware
        :return:
            None
        """
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

    def carregar_hardware_contribuido(self, indexer):
        """
        :param indexer:
            Indexador de contribuicoes
        :return:
            None
        """
        for pacote in indexer.criar_pacotes_alvo():
            if self.pacotes.get(pacote.get_id(), False):
                self.pacotes[pacote.get_id()] = pacote

    @staticmethod
    def carregar_pacote_alvo(pacote_alvo, pasta):
        """
        Carrega o pacote alvo
        :param pacote_alvo:
            Pacote de hardware
        :param pasta:
            Diretorio do pacote
        :return:
            None
        """
        pastas = os.listdir(pasta)
        if len(pastas) == 0:
            return
        for item in pastas:
            plataforma_alvo = PlataformaAlvo(item, os.path.join(pasta, item), pacote_alvo)
            pacote_alvo.get_plataformas()[item] = plataforma_alvo
            return

    def criar_menu_placas(self):
        """
        Cria o menu das placas
        :return:
            None
        """

        # Pega uma grande string contendo as placas
        placas_compativeis = listar_todas_placas_compativeis_cli()
        # Divide a string para criar uma lista
        placas_compativeis = placas_compativeis.split("\n")
        placas_compativeis_nomes = list()
        letra_corte = placas_compativeis[0].find("F")-1
        for placa in placas_compativeis:
            if placa[:int(letra_corte)].rstrip() != "":
                placas_compativeis_nomes.append([placa[:int(letra_corte)].rstrip(), placa[int(letra_corte):].rstrip()])
        placas_compativeis_nomes.pop(0)
        for placa in placas_compativeis_nomes:
            self.parent.menu_placas.addAction(QAction(placa[0], self))

        # TODO remover função

        # self.menus_personalizados = list()
        # titulos_menus_personalizados = list()
        # for pacote_alvo in self.pacotes.values():
        #     for plataforma_alvo in pacote_alvo.get_lista_plataformas():
        #         titulos_menus_personalizados += plataforma_alvo.get_menus().values()
        # for titulo_menu_personalizado in titulos_menus_personalizados:
        #     menu = QMenu(titulo_menu_personalizado)
        #     self.menus_personalizados.append(menu)
        # placas = QActionGroup(self.parent)
        # placas.setExclusive(True)
        # for pacote_alvo in self.pacotes.values():
        #     for plataforma_alvo in pacote_alvo.get_lista_plataformas():
        #         nome = plataforma_alvo.get_preferencias().get("name")
        #         self.parent.menu_placas.addAction(QAction(nome, self))
        #         self.parent.menu_placas.addAction(QAction("boi tata", self))
        #         for placa in plataforma_alvo.get_placas().values():
        #             if not placa.get_preferencias().get('hide'):
        #                 self.parent.menu_placas.addAction(placa.criar_acao(self))

    def criar_menu_portas(self):
        """
        Cria o menu das portas
        :return:
            None
        """

        # TODO Lidar com o resto da string, pegamos apenas o numero da serial para criar a lista

        # Pega uma grande string contendo as placas conectadas
        placas_conectadas = listar_todas_placas_conectadas_cli()
        # Divide a string para criar uma lista
        placas_conectadas = placas_conectadas.split("\n")
        print(placas_conectadas)
        placas_conectadas_nomes = list()
        letra_corte = placas_conectadas[0].find("T") - 1
        for placa in placas_conectadas:
            if placa[:int(letra_corte)].rstrip() != "":
                placas_conectadas_nomes.append([placa[:int(letra_corte)].rstrip(), placa[int(letra_corte):].rstrip()])
        placas_conectadas_nomes.pop(0)
        print(placas_conectadas_nomes)
        for placa in placas_conectadas_nomes:
            self.parent.menu_portas.addAction(QAction(placa[0], self))

        # TODO Remover função

        # for acao in self.parent.menu_portas.actions():
        #     self.parent.menu_portas.removeAction(acao)
        # portas = QActionGroup(self.parent)
        # portas.setExclusive(True)
        # n_portas = len(self.serial_ports())
        # if n_portas > 0:
        #     for porta in self.serial_ports():
        #         porta_acao = Porta.criar_acao(porta, self)
        #         self.parent.menu_portas.addAction(porta_acao)
        #         if n_portas == 1:
        #             Preferencias.set('serial.port', porta)
        # else:
        #     self.parent.menu_portas.addAction(QAction("Não há portas disponíveis", self))

    def criar_menu_exemplos(self):
        """
        Cria o menu exemplos
        :return:
            None
        """
        caminho_exemplos = os.path.join('recursos', 'exemplos')
        pastas_exemplo = [x for x in os.listdir(caminho_exemplos) if os.path.isdir(os.path.join(caminho_exemplos, x))]
        pastas_exemplo.sort()
        for pasta_exemplo in pastas_exemplo:
            menu = self.parent.menu_exemplos.addMenu(pasta_exemplo)
            for exemplo in os.listdir(os.path.join(caminho_exemplos, pasta_exemplo)):
                exemplo_acao = QAction(exemplo, self)
                caminho_exemplo = os.path.join(caminho_exemplos, pasta_exemplo, exemplo, exemplo + ".brpp")
                menu.addAction(exemplo_acao)
                exemplo_acao.triggered.connect(functools.partial(self.abrir, caminho_exemplo, True))

    def on_troca_placa_ou_porta(self):
        """
        Troca a placa
        :return:
            None
        """
        plataforma = self.get_plataforma_alvo()
        pastas_bibliotecas = list()
        # if plataforma:
        # core = self.get_preferencias_placa()
        pasta_plataforma = plataforma.get_pasta()
        pastas_bibliotecas.append(os.path.join(pasta_plataforma, 'libraries'))
        pastas_bibliotecas.append(os.path.join(get_caminho_padrao(), 'bibliotecas'))

    def get_preferencias_placa(self):
        """
        Busca as preferencias da palca que esta sendo utilizada
        :return prefs:
            Retorna as preferencias
        """
        placa_alvo = self.get_placa_alvo()
        if placa_alvo is None:
            return None
        id_placa = placa_alvo.get_id()
        prefs = placa_alvo.get_preferencias()
        nome_extendido = prefs.get("name")
        for id_menu in placa_alvo.get_ids_menus():
            if not placa_alvo.tem_menu(id_menu):
                continue
            entrada = Preferencias.get("custom_" + id_menu)
            if entrada is not None and entrada.startswith(id_placa):
                id_selecao = entrada[len(id_placa) + 1:]
                prefs.update(placa_alvo.get_preferencias_menu(id_menu, id_selecao))
                nome_extendido += ", " + placa_alvo.get_label_menu(id_menu, id_selecao)
        prefs['name'] = nome_extendido
        ferramentas = list()
        plataforma = self.indexer.get_plataforma_contribuida(self.get_plataforma_alvo())
        if plataforma is not None:
            ferramentas.extend(plataforma.get_ferramentas_resolvidas())

        core = prefs.get("build.core")
        if core is not None and core.__contains__(":"):
            separado = core.split(":")
            referenciada = self.get_plataforma_atual_do_pacote(separado[0])
            if referenciada is not None:
                plat_referenciada = self.indexer.get_plataforma_contribuida(referenciada)
                ferramentas.extend(plat_referenciada.get_ferramentas_resolvidas())
        prefix = "runtime.tools."
        for tool in ferramentas:
            pasta = tool.get_pasta_instalada()
            caminho = os.path.abspath(pasta)
            prefs[(prefix + tool.get_nome() + ".path")] = caminho
            Preferencias.set(prefix + tool.get_nome() + ".path", caminho)
            Preferencias.set(prefix + tool.get_nome() + "-" + tool.get_versao() + ".path", caminho)
        return prefs

    def get_placa_alvo(self):
        """
        Busca a placa alvo
        :return
            placa alvo:
        """
        plataforma_alvo = self.get_plataforma_alvo()
        if plataforma_alvo:
            placa = Preferencias.get('board')
            return plataforma_alvo.get_placa(placa)

    def get_plataforma_alvo(self, pacote=None, plataforma=None):
        """
        Pega a plataforma alvo
        :param pacote:
            Pacote da plataforma
        :param plataforma:
            A plataforma
        :return plataforma_alvo:
            Plataforma alvo
        """
        if pacote is None:
            pacote = Preferencias.get('target_package')
        if plataforma is None:
            plataforma = Preferencias.get('target_platform')
        p = self.pacotes.get(pacote)
        plataforma_alvo = p.get(plataforma)
        return plataforma_alvo

    def get_plataforma_atual_do_pacote(self, pacote):
        """
        :param pacote:
            Pacote da plataforma
        :return:
            Retorna a plataforma alvo
        """
        return self.get_plataforma_alvo(pacote, Preferencias.get("target_platform"))

    def compilar(self):
        """
        Compila o codigo da aba atual
        :return:
            None
        """
        try:
            # Rastreio compilar
            compilar = event('IDE', 'compilou')
            report('UA-89373473-3', Preferencias.get("id_cliente"), compilar)
        except:
            pass
        self.log.clear()
        self.log.insertPlainText("Compilando...")
        self.salvar()
        editor = self.widget_abas.widget(self.widget_abas.currentIndex())
        caminho = editor.get_caminho()
        # Testa se a aba eh a de boas vindas
        if caminho == 0 or caminho == '':
            return None
        placa_alvo = self.get_placa_alvo()
        plataforma_alvo = placa_alvo.get_plataforma()
        pacote_alvo = plataforma_alvo.get_pacote()
        # Transforma o codigo brpp em ino
        traduzir(caminho)
        # TODO Adicionar os parametros corretos do compilar_arduino_cli
        plataforma_alvo_cli = "arduino:samd:mkr1000"
        resultado = compilar_arduino_cli(caminho, plataforma_alvo_cli, False)
        print("PRINTS DE DEBUG")
        print(f"caminho: {caminho}")
        print(f"placa_alvo: {placa_alvo}")
        print(f"plataforma_alvo: {plataforma_alvo}")
        print(f"pacote_alvo: {pacote_alvo}")
        print("FIM DE PRINTS DE DEBUG")
        # resultado = compilar_arduino_builder(caminho, placa_alvo, plataforma_alvo, pacote_alvo, self.temp_build, self.temp_cache)
        try:
            self.log.insertPlainText(str(resultado, sys.stdout.encoding))
        except UnicodeDecodeError:
            self.log.insertPlainText(
                "Não foi possível processar a saída de texto do compilador,"
                +" é possível que ele tenha compilado corretamente.")

    # TODO Apagar funcao
    def upload(self):
        """
        Compila e carrega o codigo da aba atual
        :return:
            None
        """

        editor = self.widget_abas.widget(self.widget_abas.currentIndex())
        caminho = editor.get_caminho()
        # Testa se a aba eh a de boas vindas
        if caminho == 0 or caminho == '':
            return None
        caminho = editor.get_caminho()
        # Ajustes do Arduino
        # TODO Terminar ajustes
        caminho_temp = self.temp_build
        uploader = None
        if uploader is None:
            uploader = Uploader.get_uploader_por_preferencias()
            uploader = Uploader.UploaderSerial(False)
        sucesso = False
        nome = os.path.basename(caminho).replace("brpp", "ino")
        sucesso = uploader.upload_usando_preferencias(self, caminho_temp, os.path.basename(nome))

    @staticmethod
    def serial_ports():
        """
        Lista as portas seriais disponiveis
        :raises EnvironmentError:
            Plataforma desconhecida ou nao suportada
        :returns:
            Lista das portas seriais disponiveis
        """
        if sys.platform.startswith('win'):
            ports = ['COM%s' % (i + 1) for i in range(256)]
        elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
            # this excludes your current terminal "/dev/tty"
            ports = glob.glob('/dev/tty[A-Za-z]*')
        elif sys.platform.startswith('darwin'):
            ports = glob.glob('/dev/tty.*')
        else:
            raise EnvironmentError('Unsupported platform')

        result = []
        for port in ports:
            try:
                s = serial.Serial(port)
                s.close()
                result.append(port)
            except (OSError, serial.SerialException):
                pass
        return result

    def get_menu_personalizado_placa(self, title):
        for menu in self.menus_personalizados:
            if menu.title() == title:
                return menu

    def instalar_biblioteca(self):
        caminho_bibliotecas = os.path.join(get_caminho_padrao(), "bibliotecas")
        dialogo = QFileDialog()
        dialogo.setWindowTitle("Escolher biblioteca")
        dialogo.setLabelText(QFileDialog.FileName, "Arquivo:")
        dialogo.setLabelText(QFileDialog.LookIn, "Buscar em:")
        dialogo.setLabelText(QFileDialog.FileType, "Tipo de arquivo:")
        dialogo.setLabelText(QFileDialog.Accept, "Escolher")
        dialogo.setLabelText(QFileDialog.Reject, "Cancelar")
        dialogo.setFileMode(QFileDialog.DirectoryOnly)
        dialogo.setDirectory(get_caminho_padrao())
        if dialogo.exec_() == QFileDialog.Accepted:
            caminho = dialogo.selectedUrls()[0].path()
            if (caminho.startswith("/") and os.name == 'nt'):
                caminho = caminho[1:]
            # Testa se o arquivo existe
            if os.path.exists(caminho):
                try:
                    shutil.copytree(caminho, os.path.join(caminho_bibliotecas, os.path.basename(caminho)))
                    # Directories are the same
                except shutil.Error as e:
                    print('Directory not copied. Error: %s' % e)
                    # Any error saying that the directory doesn't exist
                except OSError as e:
                    print('Directory not copied. Error: %s' % e)
            else:
                QMessageBox(QMessageBox.Warning, "Erro", "O arquivo não existe", QMessageBox.NoButton, self).show()
        else:
            return


class Porta:

    @staticmethod
    def criar_acao(porta, parent):
        """
        Cria a acao para o menu
        :param porta:
            Porta serial
        :param parent:
            widget pai
        :return acao_porta:
            Acao para o menu
        """
        acao_porta = QAction(porta, parent)
        acao_porta.triggered.connect(functools.partial(Porta.selecionar_porta, porta, parent))
        return acao_porta

    @staticmethod
    def selecionar_porta(porta, parent_):
        """
        Seleciona a porta serial
        :param porta:
            Porta serial
        :param parent_:
            widget pai
        :return: None
        """
        Preferencias.set('serial.port', porta)
        parent_.parent.placa_porta_label.setText(Preferencias.get("board") + " na " + Preferencias.get("serial.port"))

class Principal(QMainWindow):

    def __init__(self):
        super(Principal, self).__init__()

        # Cria o objeto monitor serial
        self.monitor = MonitorSerial.MonitorSerial()

        # Define as acoes
        self.acao_novo = QAction('&Novo', self)
        self.acao_abrir = QAction('Abrir', self)
        self.acao_abrir_arduino = QAction('Abrir Traducao', self)
        self.acao_exemplos = QAction('Exemplos', self)
        self.acao_sair = QAction('Sair', self)
        self.acao_fechar_aba = QAction('Fechar aba', self)
        self.acao_salvar = QAction('&Salvar', self)
        self.acao_salvar_como = QAction('Salvar como', self)
        self.acao_comentar_linha = QAction('Comentar linha', self)
        self.acao_achar = QAction('Achar...', self)
        self.acao_achar_e_substituir = QAction('Achar e substituir', self)
        self.acao_ir_para_linha = QAction('Ir para linha', self)
        self.acao_placa = QAction('Placa', self)
        self.acao_porta = QAction('Porta', self)
        self.acao_lingua = QAction('Lingua', self)
        self.acao_instalar_biblioteca = QAction('Instalar biblioteca', self)
        self.acao_monitor_serial = QAction('Monitor serial', self)
        self.acao_verificar = QAction('Verificar', self)
        self.acao_verificar_e_carregar = QAction('Verificar e carregar', self)
        self.menu_placas = QMenu('Placa')
        self.menu_portas = QMenu('Porta')
        self.menu_exemplos = QMenu('Exemplos')
        self.barra_de_status = QStatusBar()

        self.widget_central = UI.Centro(self)

        self.criar_barra_menu()

        self.init_ui()

    def init_ui(self):
        self.setStatusBar(self.barra_de_status)
        if Preferencias.get("board") is None:
            Preferencias.set("board", "uno")
        if Preferencias.get("serial.port") is None:
            Preferencias.set("serial.port", "COM1")
        self.placa_porta_label = QLabel(Preferencias.get("board") + " na " + Preferencias.get("serial.port"))
        self.barra_de_status.addPermanentWidget(self.placa_porta_label)

        self.setCentralWidget(self.widget_central)

        self.setGeometry(100, 50, 500, 550)
        self.setMinimumSize(500, 520)
        self.setWindowTitle('Br.ino ' + versao)
        self.setWindowIcon(QIcon(os.path.join('recursos', 'logo.png')))

        self.show()


    def criar_acoes(self):
        """
        Define as funcoes de resposta as acoes e conecta elas. Define atalhos de teclado
        :return:
            None
        """
        self.acao_sair.setShortcut('Ctrl+Q')
        self.acao_sair.setStatusTip('Sair da IDE do Br.ino')
        self.acao_sair.triggered.connect(self.close)
        self.acao_sair.triggered.connect(self.monitor.close)

        self.acao_fechar_aba.setShortcut('Ctrl+W')
        self.acao_fechar_aba.setStatusTip('Fechar aba atual')
        self.acao_fechar_aba.triggered.connect(self.widget_central.remover_aba)

        self.acao_novo.setShortcut("Ctrl+N")
        self.acao_novo.triggered.connect(self.widget_central.nova_aba)
        self.acao_novo.setStatusTip("Criar novo arquivo")

        self.acao_abrir.setShortcut('Ctrl+O')
        self.acao_abrir.triggered.connect(self.widget_central.abrir)
        self.acao_abrir.setStatusTip("Abrir arquivo")

        self.acao_abrir_arduino.setShortcut('Ctrl+T')
        self.acao_abrir_arduino.triggered.connect(self.widget_central.abrir_traducao)
        self.acao_abrir.setStatusTip("Abrir Tradução")

        self.acao_salvar.setShortcut('Ctrl+S')
        self.acao_salvar.triggered.connect(self.widget_central.salvar)
        self.acao_salvar.setStatusTip("Salvar arquivo")

        self.acao_salvar_como.setShortcut('Ctrl+Shift+S')
        self.acao_salvar_como.triggered.connect(self.widget_central.salvar_como)
        self.acao_salvar_como.setStatusTip("Salvar arquivo como")

        self.acao_comentar_linha.setShortcut('Ctrl+/')
        self.acao_comentar_linha.triggered.connect(self.widget_central.comentar_linha)
        self.acao_comentar_linha.setStatusTip("Comentar linha")

        self.acao_achar.setShortcut('Ctrl+F')
        self.acao_achar.triggered.connect(self.widget_central.achar)
        self.acao_achar.setStatusTip("Achar...")

        self.acao_achar_e_substituir.setShortcut('Ctrl+H')
        self.acao_achar_e_substituir.triggered.connect(self.widget_central.achar_e_substituir)
        self.acao_achar_e_substituir.setStatusTip("Achar e substituir...")

        self.acao_ir_para_linha.setShortcut('Ctrl+L')
        self.acao_ir_para_linha.triggered.connect(GerenciadorDeCodigo.ir_para_linha)
        self.acao_ir_para_linha.setStatusTip("Ir para linha...")

        self.acao_lingua.triggered.connect(GerenciadorDeLinguas.lingua)
        self.acao_lingua.setStatusTip("Opções de língua")

        self.acao_instalar_biblioteca.triggered.connect(self.widget_central.instalar_biblioteca)
        self.acao_instalar_biblioteca.setStatusTip("Instalar bilioteca")

        self.acao_monitor_serial.setShortcut('Ctrl+Shift+M')
        self.acao_monitor_serial.triggered.connect(self.abrir_serial)
        self.acao_monitor_serial.setStatusTip("Abrir monitor serial")

        self.acao_verificar.setShortcut('Ctrl+R')
        self.acao_verificar.triggered.connect(self.widget_central.compilar)
        self.acao_verificar.setStatusTip("Verificar código")

        self.acao_verificar_e_carregar.setShortcut('Ctrl+U')
        self.acao_verificar_e_carregar.triggered.connect(self.enviar_codigo)
        self.acao_verificar_e_carregar.setStatusTip("Verificar e carregar código")

    def criar_barra_menu(self):
        """
        Cria a barra menu e adiciona as funcoes nela
        :return:
            None
        """
        self.criar_acoes()

        barra_menu = self.menuBar()
        barra_menu.setNativeMenuBar(False)
        menu_arquivo = barra_menu.addMenu('Arquivo')
        menu_arquivo.addAction(self.acao_novo)
        menu_arquivo.addAction(self.acao_abrir)
        menu_arquivo.addAction(self.acao_abrir_arduino)
        menu_arquivo.addMenu(self.menu_exemplos)
        menu_arquivo.addAction(self.acao_salvar)
        menu_arquivo.addAction(self.acao_salvar_como)
        menu_arquivo.addAction(self.acao_fechar_aba)
        menu_arquivo.addAction(self.acao_sair)

        menu_editar = barra_menu.addMenu('Editar')
        menu_editar.addAction(self.acao_comentar_linha)
        menu_editar.addAction(self.acao_achar)
        menu_editar.addAction(self.acao_achar_e_substituir)
        menu_editar.addAction(self.acao_ir_para_linha)

        self.menu_ferramentas = barra_menu.addMenu('Ferramentas')
        self.menu_ferramentas.aboutToShow.connect(self.widget_central.criar_menu_portas)
        self.menu_ferramentas.addMenu(self.menu_placas)
        self.menu_ferramentas.addMenu(self.menu_portas)
        self.menu_ferramentas.addAction(self.acao_lingua)
        self.menu_ferramentas.addAction(self.acao_monitor_serial)
        self.menu_ferramentas.addAction(self.acao_instalar_biblioteca)

        menu_rascunho = barra_menu.addMenu('Rascunho')
        menu_rascunho.addAction(self.acao_verificar)
        menu_rascunho.addAction(self.acao_verificar_e_carregar)

    def abrir_serial(self):
        """
        Abre o monitor serial ou indica que a porta nao esta disponivel
        :return:
            None
        """

        # Verifica se jah hah um monitor aberto e o fecha
        if self.monitor.isVisible():
            self.monitor.close()
        if self.monitor.conectar(Preferencias.get("serial.port")):
            self.monitor.show()
            Rastreador.log_info("Monitor Serial aberto")
        else:
            QMessageBox("Erro", QMessageBox.Warning, "A porta selecionada não está disponível",
                        QMessageBox.NoButton, self).show()
            Rastreador.log_error("Porta Serial solicitada não disponível")

    def enviar_codigo(self):
        """
        Fecha o monitor serial, compila e carrega o codigo da aba atual
        :return:
            None
        """
        Rastreador.log_info("Compilando e Carregando")
        reconectar = self.monitor.desconectar()
        self.widget_central.upload()
        Rastreador.log_info("Fim do upload")
        if reconectar:
            Rastreador.log_info("Monitor Serial fechado e reconectando")
            self.abrir_serial()
            Rastreador.log_info("Monitor Serial reconectado")

    def closeEvent(self, close_event):
        """
        Fecha o programa, mas antes verifica se os arquivos foram salvos
        :param close_event:
        :return:
        """
        if self.widget_central.widget_abas.widget(0).caminho == 0:
            num_examinar = 1
        else:
            num_examinar = 0
        for num_arquivo in range(self.widget_central.widget_abas.count() - num_examinar):
            if not self.widget_central.remover_aba(num_examinar, True):
                close_event.ignore()
                return
        Rastreador.log_info("Encerrando o Br.ino")
        self.monitor.close()
        Rastreador.log_info("Monitor serial encerrado")
        Rastreador.rastrear(Rastreador.FECHAMENTO)
        Rastreador.log_info("Rastreado fechamento")
        Preferencias.gravar_preferencias()
        Rastreador.log_info("Preferências registradas, encerrando...")
        close_event.accept()
