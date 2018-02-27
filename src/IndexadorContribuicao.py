import os

class IndexadorContribuicao():
    def __init__(self, pasta_prefs, pasta_hardware):
        self.pasta_prefs = pasta_prefs
        self.pasta_hardware = pasta_hardware
        pasta_pacotes = os.path.join(pasta_prefs, 'packages')

        self.index = None
        pass

    def parse_index(self):
        self.merge_contribuicoes(os.path.join(self.pasta_hardware, "package_index_bundled.json"))

    def merge_contribuicoes(self, path):
        if not os.path.exists(path):
            return
        indice_contribuicoes = self.parse_index(path)
        for pacote_contribuido in indice_contribuicoes.get_pacotes():
            pass

    def get_plataforma_contribuida(self, plataforma_alvo):
        for plataforma in self.get_plataformas_instaladas():
            if plataforma.get_pasta_instalada() == plataforma_alvo.get_pasta():
                return plataforma
        return None

    def get_plataformas_instaladas(self):
        if self.index is None:
            return list()
        return self.index.get_plataformas_instaladas()
