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

import ntpath
# from google_measurement_protocol import event, report
import functools
import shutil
import sys
from zipfile import ZipFile

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QTextCursor, QIcon
from PyQt5.QtWidgets import (QMainWindow, QAction, QMenu, QStatusBar, QMessageBox, QLabel, QWidget, QGridLayout,
                             QPlainTextEdit, QTabWidget, QPushButton, QFileDialog, QInputDialog, QErrorMessage, QComboBox, QToolBar)

import GerenciadorDeLinguas
import MonitorSerial
import Rastreador
import EditorDeTexto
import Menu
from BoasVindas import BoasVindas
from Integracao_arduino_cli import *
from GerenciadorDeKeywords import traduzir
from Main import get_caminho_padrao

class Centro(QWidget):
    '''
    Classe da IDE que compoe o editor de textos, o centro dela. Nessa parte onde ficam os codigos que estao sendo
    editados e as abas.
    '''
    def __init__(self, parent=None):
        super(Centro, self).__init__()
        self.widget_abas = None
        self.menu = None
        self.indexer = None
        self.parent = parent
        self.pacotes = dict()
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
        if self.criar_menu_placas():
            QMessageBox(QMessageBox.Warning, "Nenhuma placa disponivel", "Percebemos que você não tem nenhuma placa instalada, iremos instalar algumas para você. Para instalar mais placas acesse 'Ferramentas>Instalar Placa' e insira o nome da placa que deseja instalar.", QMessageBox.NoButton, self).show()
            instalar_placa("arduino:avr")
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
            Rastreador.log_info("Aberta aba %s" % editor.get_nome())
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
        texto, ok = QInputDialog.getText(self, "Buscar", "Achar:")
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
        texto, ok = QInputDialog.getText(self, "Achar", "Achar:")
        subs, ok = QInputDialog.getText(self, "Substituir", "Substituir:")
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

    def criar_menu_placas(self):
        """
        Cria o menu das placas
        :return:
            None
        """
        # Pega uma grande string contendo as placas
        placas_compativeis = listar_todas_placas_compativeis_cli()
        print(placas_compativeis)
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
        print(placas_compativeis_nomes)
        # Verifica se ha placas disponiveis
        if not placas_compativeis_nomes:
            # Se n houver placas disponiveis retorna 0
            return 1
        else:
            for placa in placas_compativeis_nomes:
                action = QAction(str(placa[0]), self)
                action.triggered.connect(lambda chk, placa=placa: self.define_placa_alvo(placa))
                self.parent.menu_placas.addAction(action)
            return 0

    def define_placa_alvo(self, placa):
        """
        Acao que e chamada quando uma placa e selecionada no menu "menu_placas". Ela pega a placa selecionada (nome e codigo) e salva como placa alvo
        :return:
            None
        """
        print(placa)
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
        if len(portas_conectadas_nomes) > 0:
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
        # Verifica se a placa para upload está selecionada. Caso nao esteja seleciona a placa Uno e usada
        try:
            if self.placa_alvo:
                self.define_placa_alvo(['Arduino Uno', ' arduino:avr:uno'])
        except:
            self.define_placa_alvo(['Arduino Uno', ' arduino:avr:uno'])
        resultado = compilar_arduino_cli(caminho, self.placa_alvo[1], False, None)
        try:
            self.log.insertPlainText(str(resultado, sys.stdout.encoding))
        except UnicodeDecodeError:
            self.log.insertPlainText(
                "Não foi possível processar a saída de texto do compilador,"
                + " é possível que ele tenha compilado corretamente.")

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

        # Verifica se a porta para upload está selecionada. Caso nao esteja seleciona a primeira da lista
        try:
            if not self.porta_alvo:
                self.define_porta_alvo(self.parent.menu_selecao_porta.currentText())
        except:
            self.define_porta_alvo(self.parent.menu_selecao_porta.currentText())

        # Verifica se a placa para upload está selecionada. Caso nao esteja seleciona a placa Uno e usada
        try:
            if not self.placa_alvo:
                self.define_placa_alvo(['Arduino Uno', ' arduino:avr:uno'])
        except:
            self.define_placa_alvo(['Arduino Uno', ' arduino:avr:uno'])

        resultado = compilar_arduino_cli(caminho, self.placa_alvo[1], True, self.porta_alvo)
        try:
            self.log.insertPlainText(str(resultado, sys.stdout.encoding))
        except UnicodeDecodeError:
            self.log.insertPlainText(
                "Não foi possível processar a saída de texto do compilador,"
                + " é possível que ele tenha compilado corretamente.")

    def instalar_placa(self):
        """
        Instala a placa Arduino a ser inserida em pop_up
        :returns:
            None
        """
        # Cria o pop-up para escolha da placa a ser instalada
        nome_placa_instalar = QInputDialog.getText(self, 'Instalar placa', 'Qual o nome da placa que você deseja instalar?')
        self.log.clear()
        self.log.insertPlainText("Carregando placas disponíveis....\n")
        # busca placas com o nome inserido
        placa_instalar = procurar_placas(nome_placa_instalar[0]).split("\n")
        # Cria a lista com a saida
        lista_placa_instalar = list()
        letra_corte = placa_instalar[0].find("F") - 1
        for placa in placa_instalar:
            if placa[:int(letra_corte)].rstrip() != "":
                lista_placa_instalar.append([placa[:int(letra_corte)].rstrip(), placa[int(letra_corte):].rstrip()])
        lista_placa_instalar.pop(0)
        print(lista_placa_instalar)
        dialogo_lista_placa = list()
        for i in range(len(lista_placa_instalar)):
            dialogo_lista_placa.append(lista_placa_instalar[i][0])
        # Se a lista nao for vazia cria um pop-up para escolha da placa
        if lista_placa_instalar:
            nome_placa_instalar = QInputDialog.getItem(self, 'Instalar placa', 'Selecione a placa a ser instalada:', dialogo_lista_placa)
            if nome_placa_instalar[1]:
                for i in range(len(lista_placa_instalar)):
                    if nome_placa_instalar[0] == lista_placa_instalar[i][0]:
                        placa_lista = lista_placa_instalar[i][1].split()
                        placa = placa_lista[-1]
                        self.log.clear()
                        self.log.insertPlainText(f"Instalando a placa {nome_placa_instalar[0]}")
                        self.log.insertPlainText(str(instalar_placa(placa)))
                        self.criar_menu_placas()


        # Se nao levanta um alerta de erro
        else:
            # TODO Melhorar aparencia da QErrorMessage
            error_dialog_placa = QErrorMessage()
            error_dialog_placa.setWindowTitle('Placa solicitada indisponível.')
            error_dialog_placa.showMessage('Placa não encontrada. Verifique o nome e tente novamente.')
            error_dialog_placa.exec_()
            Rastreador.log_error("Placa solicitada não disponível")
        print(nome_placa_instalar[0])


    def instalar_biblioteca_arduino_cli(self):
        """
        Instala a biblioteca Arduino pelo arduino cli a ser selecionada em um pop_up
        :returns:
            None
        """
        # Cria o pop-up para escolha da biblioteca a ser instalada
        nome_biblioteca_instalar = QInputDialog.getText(self, 'Instalar biblioteca por nome',
                                                   'Qual o nome da biblioteca que você deseja instalar?')
        self.log.clear()
        self.log.insertPlainText("Carregando bibliotecas disponíveis....\n")
        # busca biblioteca com o nome inserido
        biblioteca_instalar = procurar_bibliotecas(nome_biblioteca_instalar[0]).split("\n")
        print(biblioteca_instalar)
        # TODO Resolver formato de apresentacao das bibliotecas disponiveis, mostrar mais dados
        dialogo_lista_biblioteca = list()
        # Verifica se foi encontrada alguma biblioteca com o nome inserido
        if "No libraries matching your search." in biblioteca_instalar:
            # TODO Melhorar aparencia da QErrorMessage
            error_dialog_biblioteca = QErrorMessage()
            error_dialog_biblioteca.setWindowTitle('Biblioteca solicitada indisponível')
            error_dialog_biblioteca.showMessage('Biblioteca não encontrada. Verifique o nome e tente novamente.')
            error_dialog_biblioteca.exec_()
            Rastreador.log_error("Biblioteca solicitada não disponível")
        else:
            for item_biblioteca_instalar in biblioteca_instalar:
                if "Name" in item_biblioteca_instalar:
                    dialogo_lista_biblioteca.append(item_biblioteca_instalar.replace('Name: "', "")[:-1])
            nome_biblioteca_instalar = QInputDialog.getItem(self, 'Instalar biblioteca', 'Selecione a biblioteca a ser instalada:',
                                                       dialogo_lista_biblioteca)
            if nome_biblioteca_instalar[1]:
                Rastreador.log_info("Instalando biblioteca CLI")
                self.log.clear()
                self.log.insertPlainText(f"Instalando biblioteca {nome_biblioteca_instalar[0]}...\n\n")
                self.log.insertPlainText(str(instalar_biblioteca('"' + nome_biblioteca_instalar[0] + '"')))


    def instalar_biblioteca_por_arquivo(self):
        """
        Instala a biblioteca Arduino .zip a ser selecionada em pop_up. Essa fucao permite vc escolher o arquivo que
         será extraido e copiado para a pasta correta.
        :returns:
            None
        """
        caminho_bibliotecas = os.path.join(get_caminho_padrao(), "bibliotecas")
        dialogo = QFileDialog()
        dialogo.setWindowTitle("Escolher biblioteca")
        dialogo.setLabelText(QFileDialog.FileName, "Arquivo:")
        dialogo.setLabelText(QFileDialog.LookIn, "Buscar em:")
        dialogo.setLabelText(QFileDialog.FileType, "Tipo de arquivo:")
        dialogo.setLabelText(QFileDialog.Accept, "Escolher")
        dialogo.setLabelText(QFileDialog.Reject, "Cancelar")
        dialogo.setNameFilters(["Arquivo zip (*.zip)", "Todos arquivos (*)"])
        dialogo.selectNameFilter("Arquivo zip (*.zip)")
        dialogo.setDirectory(get_caminho_padrao())
        if dialogo.exec_() == QFileDialog.Accepted:
            caminho = dialogo.selectedUrls()[0].path()
            if caminho.startswith("/") and os.name == 'nt':
                caminho = caminho[1:]
            # Testa se o arquivo existe
            if os.path.exists(caminho):
                try:
                    # shutil.copy(caminho, os.path.join(caminho_bibliotecas, os.path.basename(caminho)))
                    # Create a ZipFile Object and load sample.zip in it
                    # TODO Adicionar os exemplos das bibliotecas na IDE
                    with ZipFile(caminho, 'r') as zipObj:
                        # Extract all the contents of zip file in current directory
                        zipObj.extractall(caminho_bibliotecas)
                    # Directories are the same
                except shutil.Error as e:
                    print('Arquivo nao copiado. Erro: %s' % e)
                    # Any error saying that the directory doesn't exist
                except OSError as e:
                    print('Arquivo nao copiado. Erro: %s' % e)
            else:
                QMessageBox(QMessageBox.Warning, "Erro", "O arquivo não existe", QMessageBox.NoButton, self).show()
        else:
            return


class Principal(QMainWindow):
    def __init__(self):
        super(Principal, self).__init__()

        self.versao = '3.0.8'

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
        self.acao_instalar_biblioteca_por_arquivo = QAction('Instalar biblioteca por arquivo', self)
        self.acao_instalar_biblioteca_arduino_cli = QAction('Instalar biblioteca por nome', self)
        self.acao_instalar_placa = QAction('Instalar placa', self)
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
        self.setWindowTitle('Br.ino ' + self.versao)
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
        self.acao_ir_para_linha.triggered.connect(EditorDeTexto.ir_para_linha)
        self.acao_ir_para_linha.setStatusTip("Ir para linha...")

        self.acao_lingua.triggered.connect(GerenciadorDeLinguas.lingua)
        self.acao_lingua.setStatusTip("Opções de língua")

        self.acao_instalar_biblioteca_por_arquivo.triggered.connect(self.widget_central.instalar_biblioteca_por_arquivo)
        self.acao_instalar_biblioteca_por_arquivo.setStatusTip("Instalar bilioteca por aquivo zip")

        self.acao_instalar_biblioteca_arduino_cli.triggered.connect(self.widget_central.instalar_biblioteca_arduino_cli)
        self.acao_instalar_biblioteca_arduino_cli.setStatusTip("Instalar bilioteca por nome")

        self.acao_instalar_placa.triggered.connect(self.widget_central.instalar_placa)
        self.acao_instalar_placa.setStatusTip("Instalar placa")

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
        self.menu_ferramentas.addMenu(self.menu_placas)
        self.menu_ferramentas.addAction(self.acao_lingua)
        self.menu_ferramentas.addAction(self.acao_monitor_serial)
        self.menu_ferramentas.addAction(self.acao_instalar_biblioteca_por_arquivo)
        self.menu_ferramentas.addAction(self.acao_instalar_biblioteca_arduino_cli)
        self.menu_ferramentas.addAction(self.acao_instalar_placa)

        menu_rascunho = barra_menu.addMenu('Rascunho')
        menu_rascunho.addAction(self.acao_verificar)
        menu_rascunho.addAction(self.acao_verificar_e_carregar)

        self.barra_superior.addWidget(barra_menu)
        self.barra_superior.addWidget(QLabel("Porta: "))

        self.menu_selecao_porta = QComboBox()

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

        print("Chamando monitor serial")
        # Verifica se a porta para upload está selecionada. Caso nao esteja seleciona a primeira da lista
        try:
            if not self.widget_central.porta_alvo:
                self.widget_central.define_porta_alvo(self.menu_selecao_porta.currentText())
        except:
            self.widget_central.define_porta_alvo(self.menu_selecao_porta.currentText())
            
        if self.monitor.conectar(self.widget_central.porta_alvo):
            self.monitor.show()
            Rastreador.log_info("Monitor Serial aberto")
        else:
            # TODO Melhorar aparencia da QErrorMessage
            error_dialog = QErrorMessage()
            error_dialog.setWindowTitle('Porta serial indisponível')
            error_dialog.showMessage('A porta serial selecionada não está disponível.')
            error_dialog.exec_()
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
