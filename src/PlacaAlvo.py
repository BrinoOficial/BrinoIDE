#!/usr/bin/python
# -*- coding: utf-8 -*-

# TODO Apagar arquivo

"""
Br.ino Qt placa alvo

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

    Codigo fonte baseado no codigo do arduino

website: brino.cc
modificado por: Mateus Berardo
email: mateus.berardo@brino.cc
modificado por: Victor Rodrigues Pacheco
email: victor.pacheco@brino.cc
"""

import functools
import os

from PyQt5.QtWidgets import QAction

import MapaUtils
import Preferencias


class PlacaAlvo:
    def __init__(self, nome, prefs, parent):
        self.plataforma = parent
        self.id_ = nome
        self.prefs = prefs
        self.menu_opcoes = dict()

        menus = MapaUtils.primeiro_nivel(prefs).get('menu')
        if menus:
            self.menu_opcoes = MapaUtils.primeiro_nivel(menus)
        if 'build.board' not in self.prefs.keys():
            placa = parent.get_id() + "_" + nome
            placa = placa.upper()
            prefs['build.board'] = placa

    def get_preferencias(self):
        return self.prefs

    def get_id(self):
        return self.id_

    def get_plataforma(self):
        return self.plataforma

    def criar_acao(self, parent):
        acao_placa = QAction(PlacaAlvo.capitalizar(self.get_id()), parent)
        acao_placa.triggered.connect(functools.partial(self.selecionar_placa, self, parent))
        return acao_placa

    @staticmethod
    def selecionar_placa(arg, parent):
        plataforma_alvo = arg.get_plataforma()
        pacote_alvo = plataforma_alvo.get_pacote()
        Preferencias.set("target_package", pacote_alvo.get_id())
        Preferencias.set("target_platform", plataforma_alvo.get_id())
        Preferencias.set("board", arg.get_id())
        pasta_plataforma = os.path.abspath(os.path.join('.', plataforma_alvo.get_pasta()))
        Preferencias.set("runtime.platform.path", pasta_plataforma)
        Preferencias.set('runtime.hardware.path', os.path.dirname(pasta_plataforma))
        parent.on_troca_placa_ou_porta()
        parent.parent.placa_porta_label.setText(Preferencias.get("board") + " na " + Preferencias.get("serial.port"))

        titulos_menus_personalizados = plataforma_alvo.get_menus()
        for id in titulos_menus_personalizados.keys():
            menu = parent.get_menu_personalizado_placa(titulos_menus_personalizados.get(id))
            menu.clear()
            if id in arg.menu_opcoes:
                menu_personalizado_placa = MapaUtils.dicionario_superior(arg.menu_opcoes.get(id))
                for opcao in menu_personalizado_placa.keys():
                    acao_opcao = QAction(menu_personalizado_placa.get(opcao), parent)
                    acao_opcao.triggered.connect(
                        functools.partial(PlacaAlvo.set_opcoes_personalizadas, arg.get_id(), opcao, id))
                    menu.addAction(acao_opcao)
                parent.parent.menu_ferramentas.addMenu(menu)
                acao_opcao.trigger()
            else:
                for item in parent.parent.menu_ferramentas.actions():
                    if menu == item.menu():
                        parent.parent.menu_ferramentas.removeAction(item)

                # Base.java line 1534

    @staticmethod
    def set_opcoes_personalizadas(placa, opcao, menu_id):
        Preferencias.set("custom_" + menu_id, placa + "_" + opcao)

    @staticmethod
    def capitalizar(string):
        retorno = "%s%s" % (string[0].upper(), string[1:])
        return retorno

    def get_ids_menus(self):
        return self.menu_opcoes.keys()

    def tem_menu(self, id):
        return id in self.menu_opcoes.keys()

    def get_preferencias_menu(self, id_menu, id_selecao):
        return MapaUtils.sub_tree(self.menu_opcoes.get(id_menu), id_selecao)

    def get_label_menu(self, id_menu, id_selecao):
        return self.get_labels_menu(id_menu).get(id_selecao)

    def get_labels_menu(self, id_menu):
        return MapaUtils.dicionario_superior(self.menu_opcoes.get(id_menu))
