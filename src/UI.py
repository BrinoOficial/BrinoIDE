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
from tempfile import mkdtemp
from google_measurement_protocol import event, report
import functools
import serial
import shutil
import os
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QTextCursor, QIcon
from PyQt5.QtWidgets import (QMainWindow, QAction, QMenu, QStatusBar, QMessageBox, QLabel, QWidget, QGridLayout,
                             QPlainTextEdit, QTabWidget, QPushButton, QFileDialog, QInputDialog, QComboBox, QToolBar,
                             QToolButton, QHBoxLayout, QApplication)

import GerenciadorDeCodigo
import GerenciadorDeLinguas
import MonitorSerial
import Rastreador
import EditorDeTexto
import Menu
from BoasVindas import BoasVindas
from integracao_arduino_cli import *
from GerenciadorDeKeywords import traduzir
from Main import get_caminho_padrao


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

        # Cria menu de placas
        self.criar_menu_placas()
        self.criar_menu_exemplos()

        # Adiciona a aba de boas vindas
        self.widget_abas.addTab(BoasVindas(self), "Bem-Vindo")
        self.show()
        Rastreador.log_info("WidgetCentral Carregado")

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
        self.placas_compativeis_nomes = placas_compativeis_nomes
        self.parent.menu_placas.clear()
        for placa in placas_compativeis_nomes:
            action = QAction(placa[0], self)
            action.triggered.connect(lambda chk, placa=placa: self.define_placa_alvo(placa))
            self.parent.menu_placas.addAction(action)

    def define_placa_alvo(self, placa):
        """
        Acao que e chamada quando uma placa e selecionada no menu "menu_placas". Ela pega a placa selecionada (nome e codigo) e salva como placa alvo
        :return:
            None
        """
        self.placa_alvo = placa
        try:
            self.parent.placa_porta_label.setText(self.placa_alvo[0] + " na " + self.porta_alvo)
        except:
            self.parent.placa_porta_label.setText(self.placa_alvo[0] + ", selecione a porta")

    def criar_menu_portas(self):
        """
        Cria o menu das portas
        :return:
            None
        """
        print("Atualizando as portas no menu")
        # TODO Lidar com o resto da string, pegamos apenas o numero da serial para criar a lista

        # Pega uma grande string contendo as placas conectadas
        portas_conectadas = listar_todas_placas_conectadas_cli()
        # Divide a string para criar uma lista
        portas_conectadas = portas_conectadas.split("\n")

        portas_conectadas_nomes = list()
        letra_corte = portas_conectadas[0].find(" ")
        for porta in portas_conectadas:
            if porta[:int(letra_corte)].rstrip() != "":
                portas_conectadas_nomes.append([porta[:int(letra_corte)].rstrip(), porta[int(letra_corte):].rstrip()])
        portas_conectadas_nomes.pop(0)
        # Limpa a lista atual de portas e adiciona a nova leitura de portas conectadas
        self.parent.menu_selecao_porta.clear()
        for porta in portas_conectadas_nomes:
            self.parent.menu_selecao_porta.addItem(porta[0])

    def define_porta_alvo(self, porta):
        """
        Acao que e chamada quando uma porta e selecionada no menu "menu_portas". Ela pega a placa selecionada (nome) e salva como porta_alvo
        :return:
            None
        """
        print("Porta alvo definida")
        self.porta_alvo = porta
        try:
            self.parent.placa_porta_label.setText(self.placa_alvo[0] + " na " + self.porta_alvo)
        except:
            self.parent.placa_porta_label.setText("Selecione a placa conectada na " + self.porta_alvo)

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


    def compilar(self):
        """
        Compila o codigo da aba atual
        :return:
            None
        """
        try:
            pass
            # Rastreio compilar
            # TODO Arrumar variavel rastreio
            # compilar = event('IDE', 'compilou')
            # report('UA-89373473-3', Preferencias.get("id_cliente"), compilar)
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
        # Transforma o codigo brpp em ino
        traduzir(caminho)
        # TODO Adicionar os parametros corretos do compilar_arduino_cli
        resultado = compilar_arduino_cli(caminho, self.placa_alvo[1], False, "None")
        try:
            self.log.insertPlainText(str(resultado, sys.stdout.encoding))
        except UnicodeDecodeError:
            self.log.insertPlainText(
                "Não foi possível processar a saída de texto do compilador,"
                +" é possível que ele tenha compilado corretamente.")

    def upload(self):
        """
        Compila e carrega o codigo da aba atual
        :return:
            None
        """

        self.log.clear()
        self.log.insertPlainText("Compilando e carregando...")
        self.salvar()
        editor = self.widget_abas.widget(self.widget_abas.currentIndex())
        caminho = editor.get_caminho()
        # Testa se a aba eh a de boas vindas
        if caminho == 0 or caminho == '':
            return None
        # Transforma o codigo brpp em ino
        traduzir(caminho)
        resultado = compilar_arduino_cli(caminho, self.placa_alvo[1], True, self.porta_alvo[0])
        try:
            self.log.insertPlainText(str(resultado, sys.stdout.encoding))
        except UnicodeDecodeError:
            self.log.insertPlainText(
                "Não foi possível processar a saída de texto do compilador,"
                + " é possível que ele tenha compilado corretamente.")

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

        self.widget_central = Centro(self)

        self.criar_barra_menu()

        self.init_ui()

    def init_ui(self):
        self.setStatusBar(self.barra_de_status)
        self.placa_porta_label = QLabel("Selecione sua placa e porta")
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
        Cria a barra do menu superior e adiciona as funcoes nela
        :return:
            None
        """
        self.criar_acoes()

        # Cria a QToolBar que engloba todas as funcionalidades do menu superior
        self.barra_superior = QToolBar()
        self.barra_superior.setMovable(False)
        self.barra_superior.setContentsMargins(0, 0, 0, 0)


        # Cria a barra de menu que ira ser adicionada a barra_superior
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
        # self.menu_ferramentas.aboutToShow.connect(self.widget_central.criar_menu_portas)
        self.menu_ferramentas.addMenu(self.menu_placas)
        self.menu_ferramentas.addMenu(self.menu_portas)
        self.menu_ferramentas.addAction(self.acao_lingua)
        self.menu_ferramentas.addAction(self.acao_monitor_serial)
        self.menu_ferramentas.addAction(self.acao_instalar_biblioteca)

        menu_rascunho = barra_menu.addMenu('Rascunho')
        menu_rascunho.addAction(self.acao_verificar)
        menu_rascunho.addAction(self.acao_verificar_e_carregar)

        self.barra_superior.addWidget(barra_menu)


        self.menu_selecao_porta = QComboBox()
        # TODO Resolver placeholder n funcionando
        self.menu_selecao_porta.setPlaceholderText("Porta")
        self.menu_selecao_porta.activated[str].connect(self.widget_central.define_porta_alvo)

        self.barra_superior.addWidget(self.menu_selecao_porta)


        self.addToolBar(self.barra_superior)

    def abrir_serial(self):
        """
        Abre o monitor serial ou indica que a porta nao esta disponivel
        :return:
            None
        """

        # Verifica se jah hah um monitor aberto e o fecha
        if self.monitor.isVisible():
            self.monitor.close()
        # TODO Resolver porta serial
        if self.monitor.conectar("COM1"):
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
        close_event.accept()
