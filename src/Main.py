#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QApplication, QAction

import GerenciadorDeArquivos
import GerenciadorDeCodigo
import GerenciadorDeLinguas
import MonitorSerial
import UI

"""
Br.ino Qt Main

Codigo da janela principal da IDE Br.ino
em PyQt5 (python 2.7)

    setaCima.png, setaBaixo.png, setaDireita.png e setaEsquerda.png 
    made by Dave Gandy
    Site: https://www.flaticon.com/authors/dave-gandy
    is licensed by: http://creativecommons.org/licenses/by/3.0/"

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

versao = '3.0.0'


class Principal(QMainWindow):

    def __init__(self):
        super(Principal, self).__init__()

        self.acao_novo = 0
        self.acao_abrir = 0
        self.acao_exemplos = 0
        self.acao_sair = 0
        self.acao_salvar = 0
        self.acao_salvar_como = 0
        self.acao_comentar_linha = 0
        self.acao_achar = 0
        self.acao_achar_e_substituir = 0
        self.acao_ir_para_linha = 0
        self.acao_placa = 0
        self.acao_porta = 0
        self.acao_lingua = 0
        self.acao_monitor_serial = 0
        self.acao_verificar = 0
        self.acao_verificar_e_carregar = 0

        self.init_ui()

    def init_ui(self):
        self.criar_barra_menu()

        self.setCentralWidget(UI.Centro())

        self.setGeometry(100, 50, 500, 550)
        self.setMinimumWidth(500)
        self.setMinimumHeight(520)
        self.setWindowTitle('Br.ino ' + versao)
        self.setWindowIcon(QIcon(os.path.join('recursos', 'logo.png')))
        self.show()

    def criar_acoes(self):
        acao_sair = QAction('Sair', self)
        acao_sair.setShortcut('Ctrl+Q')
        acao_sair.setStatusTip('Sair da IDE do Br.ino')
        acao_sair.triggered.connect(self.close)
        self.acao_sair = acao_sair

        acao_novo = QAction('&Novo', self)
        acao_novo.setShortcut("Ctrl+N")
        acao_novo.triggered.connect(GerenciadorDeArquivos.novo)
        self.acao_novo = acao_novo

        acao_abrir = QAction('Abrir', self)
        acao_abrir.setShortcut('Ctrl+O')
        acao_abrir.triggered.connect(GerenciadorDeArquivos.abrir)
        self.acao_abrir = acao_abrir

        acao_exemplos = QAction('Exemplos', self)
        acao_exemplos.triggered.connect(GerenciadorDeArquivos.exemplos)
        self.acao_exemplos = acao_exemplos

        acao_salvar = QAction('&Salvar', self)
        acao_salvar.setShortcut('Ctrl+S')
        acao_salvar.triggered.connect(GerenciadorDeArquivos.salvar)
        self.acao_salvar = acao_salvar

        acao_salvar_como = QAction('Salvar como', self)
        acao_salvar_como.setShortcut('Ctrl+B')
        acao_salvar_como.triggered.connect(GerenciadorDeArquivos.salvar_como)
        self.acao_salvar_como = acao_salvar_como

        acao_comentar_linha = QAction('Comentar linha', self)
        acao_comentar_linha.setShortcut('Ctrl+/')
        acao_comentar_linha.triggered.connect(GerenciadorDeCodigo.comentar_linha)
        self.acao_comentar_linha = acao_comentar_linha

        acao_achar = QAction('Achar...', self)
        acao_achar.setShortcut('Ctrl+F')
        acao_achar.triggered.connect(GerenciadorDeCodigo.achar)
        self.acao_achar = acao_achar

        acao_achar_e_substituir = QAction('Achar e substituir', self)
        acao_achar_e_substituir.setShortcut('Ctrl+H')
        acao_achar_e_substituir.triggered.connect(GerenciadorDeCodigo.achar_e_substituir)
        self.acao_achar_e_substituir = acao_achar_e_substituir

        acao_ir_para_linha = QAction('Ir para linha', self)
        acao_ir_para_linha.setShortcut('Ctrl+L')
        acao_ir_para_linha.triggered.connect(GerenciadorDeCodigo.ir_para_linha)
        self.acao_ir_para_linha = acao_ir_para_linha

        acao_placa = QAction('Placa', self)
        acao_placa.triggered.connect(GerenciadorDeCodigo.placa)
        self.acao_placa = acao_placa

        acao_porta = QAction('Porta', self)
        acao_porta.triggered.connect(GerenciadorDeCodigo.porta)
        self.acao_porta = acao_porta

        acao_lingua = QAction('Lingua', self)
        acao_lingua.triggered.connect(GerenciadorDeLinguas.lingua)
        self.acao_lingua = acao_lingua

        acao_monitor_serial = QAction('Monitor serial', self)
        acao_monitor_serial.setShortcut('Ctrl+Shift+M')
        acao_monitor_serial.triggered.connect(MonitorSerial.monitor_serial)
        self.acao_monitor_serial = acao_monitor_serial

        acao_verificar = QAction('Verificar', self)
        acao_verificar.setShortcut('Ctrl+R')
        acao_verificar.triggered.connect(GerenciadorDeCodigo.verificar)
        self.acao_verificar = acao_verificar

        acao_verificar_e_carregar = QAction('Verificar e carregar', self)
        acao_verificar_e_carregar.setShortcut('Ctrl+U')
        acao_verificar_e_carregar.triggered.connect(GerenciadorDeCodigo.verificar_e_carregar)
        self.acao_verificar_e_carregar = acao_verificar_e_carregar


    def criar_barra_menu(self):
        self.criar_acoes()

        barra_menu = self.menuBar()
        menu_arquivo = barra_menu.addMenu('&Arquivo')
        menu_arquivo.addAction(self.acao_novo)
        menu_arquivo.addAction(self.acao_abrir)
        menu_exemplos = menu_arquivo.addMenu('Exemplos')
        menu_arquivo.addAction(self.acao_salvar)
        menu_arquivo.addAction(self.acao_salvar_como)
        menu_arquivo.addAction(self.acao_sair)

        menu_editar = barra_menu.addMenu('&Editar')
        menu_editar.addAction(self.acao_comentar_linha)
        menu_editar.addAction(self.acao_achar)
        menu_editar.addAction(self.acao_achar_e_substituir)
        menu_editar.addAction(self.acao_ir_para_linha)

        menu_ferramentas = barra_menu.addMenu('Ferramentas')
        menu_placa = menu_ferramentas.addMenu('Placa')
        menu_porta = menu_ferramentas.addMenu('Porta')
        menu_ferramentas.addAction(self.acao_lingua)
        menu_ferramentas.addAction(self.acao_monitor_serial)

        menu_rascunho = barra_menu.addMenu('Rascunho')
        menu_rascunho.addAction(self.acao_verificar)
        menu_rascunho.addAction(self.acao_verificar_e_carregar)


def main():
    app = QApplication(sys.argv)
    principal = Principal()
    principal.show()
    app.setStyleSheet("""QMainWindow {
                             background: '#252525';
                         }
                         QMenu{
                             background: '#252525';
                         }
                         QMenu::item {
                             background: '#252525';
                         } 
                         QMenu::item:selected{
                             background: '#101010';
                         }
                         QMenuBar {
                            background: '#252525';
                         }
                         QMenuBar::item {
                            background: '#252525';
                         } 
                         QMenuBar::item:selected{
                            background: '#101010';
                         }
                         QPlainTextEdit{
                            background: '#252525';
                            border: None;
                            color: '#efefef';
                            selection-background-color: '#454545';
                         }
                         QScrollBar:vertical {
                            width: 10px;
                            margin: 2px 0 2px 0;
                          }
                         QScrollBar::handle:vertical {
                            min-height: 5px;
                            background: #5cb50d;
                            border-radius: 5px;
                         }
                         QScrollBar::add-line:vertical {
                            height: 0px;
                            subcontrol-position: bottom;
                            subcontrol-origin: margin;
                         }
                         QScrollBar::sub-line:vertical {
                            height: 0px;
                            subcontrol-position: top;
                            subcontrol-origin: margin;
                         }
                         QScrollBar:horizontal {
                            height: 10px;
                            margin: 0px 2px 0px 2px;
                          }
                         QScrollBar::handle:horizontal {
                            min-width: 5px;
                            background: #5cb50d;
                            border-radius: 5px;
                         }
                         QScrollBar::add-line:horizontal {
                            width: 0px;
                            subcontrol-position: bottom;
                            subcontrol-origin: margin;
                         }
                         QScrollBar::sub-line:horizontal {
                            width: 0px;
                            subcontrol-position: top;
                            subcontrol-origin: margin;
                         }
                         QDialog{
                            background:#252525;
                            filedialog-listview-icon: url(recursos/listaFoco.png);
                            filedialog-new-directory-icon: url(recursos/NovaPasta.png);
                            filedialog-parent-directory-icon: url(recursos/pastaPrincipal.png);
                            filedialog-detailedview-icon: url(recursos/detalhesFoco.png);
                            filedialog-contentsview-icon: url(recursos/pasta.png)
                         }
                         QDialog QListView{
                            background:#101010;
                            margin:0;
                            padding:5;        
                            border-radius:5px;
                            border-color:#101010;                    
                         }
                         QListView QScrollBar:vertical{
                            background:#101010;                            
                         }
                         QListView QScrollBar:horizontal{
                            background:#101010;                            
                         }
                         QHeaderView{
                            background-color:#252525;
                            border-radius:5px;                    
                         }
                         QHeaderView::section{
                            background-color:#252525;
                            color:#efefef;
                            border-radius:5px;                    
                         }
                         QDialog QTreeView::branch{
                            background:#101010;
                            border-color:#101010;                    
                         }
                         QDialog QTreeView{
                            background:#101010;
                            margin:0;
                            padding:5;        
                            border-radius:5px;
                            border-color:#101010;                    
                         }
                         QDialog QLabel{
                            color:#efefef;
                         }
                         QDialog QComboBox{
                            height:25px;
                            background:#101010;
                            border-radius:5px;
                         }
                         QComboBox{
                            selection-background-color: #5cb50d;
                         }
                         QDialog QComboBox::down-arrow{
                            border: 0;
                            height: 50px;
                            image: url(recursos/setaBaixo.png);
                         }
                         QComboBox::drop-down{                        
                            border: 0px;
                         }
                         QDialog QLineEdit{
                            height:25px;
                            background:#101010;
                            border-radius:5px;
                         }
                         QDialog QPushButton{
                            background:#5cb50d;
                            border-radius:5px;
                            height:30px;
                            width:70px;
                            color:#efefef;
                         }
                         QTreeView QScrollBar:vertical{
                            background:#101010;                            
                         }
                         QTreeView QScrollBar:horizontal{
                            background:#101010;                            
                         }
                         QTabBar::tab{
                            background: #101010;
                            color: #efefef;
                            border-right: 1px solid #505050;
                            padding-right: 5px;
                            padding-left: 5px;
                         }
                         QTabBar::close-button{
                            image: url(recursos/fechar.png);
                            padding: 6px;
                         }
                         QTabBar::close-button:hover{
                            image: url(recursos/fecharFoco.png);
                            padding: 4px;
                         }
                         QTabBar::tab:selected{
                            background:#252525;
                            border-top: 2px solid #5cb50d;
                         }
                         QTabWidget::pane{
                            background: #101010;
                         }
                         QTabWidget QPushButton{
                            background:#252525;
                            border:0;
                            padding:3px;
                            margin-top: 3px;
                            image: url(recursos/mais.png);
                         }
                         QTabWidget QPushButton:hover{
                            padding:0;
                            image: url(recursos/maisFoco.png);
                         }
                         
                         """)
    GerenciadorDeArquivos.novo(False)
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
