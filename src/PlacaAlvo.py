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

        menus = MapaUtils.primeiro_nivel(prefs).get('menu')
        if menus:
            menu_opcoes = MapaUtils.primeiro_nivel(menus)
        if not 'build.board' in self.prefs.keys():
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
        print(pasta_plataforma)
        Preferencias.set("runtime.platform.path", pasta_plataforma)
        Preferencias.set('runtime.hardware.path', os.path.dirname(pasta_plataforma))
        parent.on_troca_placa_ou_porta()

    @staticmethod
    def capitalizar(string):
        retorno = "%s%s" % (string[0].upper(), string[1:])
        return retorno
