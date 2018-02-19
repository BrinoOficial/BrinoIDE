#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
from PyQt5.QtWidgets import QFileDialog, QInputDialog
import EditorDeTexto
import UI

"""
Br.ino Qt Gerenciador de Arquivos

Codigo gerenciador de arquivos da IDE Br.ino
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

caminho = ""
caminho_padrao = ""


def abrir(parent):
    dialogo = QFileDialog()
    dialogo.setWindowTitle("Abrir arquivo")
    dialogo.setLabelText(QFileDialog.FileName, "Arquivo:")
    dialogo.setLabelText(QFileDialog.LookIn, "Buscar em:")
    dialogo.setLabelText(QFileDialog.FileType, "Tipo de arquivo:")
    dialogo.setLabelText(QFileDialog.Accept, "Abrir")
    dialogo.setLabelText(QFileDialog.Reject, "Cancelar")
    dialogo.setNameFilters(["Rascunhos Br.ino (*.brpp)", "Rascunhos Arduino (*.ino)"])
    dialogo.selectNameFilter("Rascunhos Br.ino (*.brpp)")
    if dialogo.exec_() == QFileDialog.Accepted:
        global caminho
        caminho = dialogo.selectedFiles()[0]
        with open(caminho) as arquivo:
            EditorDeTexto.set_texto(arquivo.read())


def exemplos():
    # TODO abrir exemplos
    print "exemplos"


def salvar():
    global caminho
    if caminho != "":
        with open(caminho, "w") as arquivo:
            arquivo.write(EditorDeTexto.get_texto())
    else:
        salvar_como()


def novo(arg, text):
    pass

def salvar_como():
    # TODO salvar como
    print "Salvando como"




