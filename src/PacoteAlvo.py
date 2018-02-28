class PacoteAlvo:

    def __init__(self, id_):
        self.id_ = id_
        self.plataformas = dict()

    def get_plataformas(self):
        return self.plataformas

    def get_lista_plataformas(self):
        return self.plataformas.values()

    def get(self, plataforma):
        return self.plataformas.get(plataforma)

    def tem_plataforma(self, plataforma):
        return self.plataformas.has_key(plataforma.get_id())

    def get_id(self):
        return self.id_

    def adicionar_plataforma(self, plataforma):
        self.plataformas[plataforma.get_id()] = plataforma
