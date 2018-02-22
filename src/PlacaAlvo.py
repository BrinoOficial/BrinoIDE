import MapaUtils


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

    def get_nome(self):
        return self.id_
