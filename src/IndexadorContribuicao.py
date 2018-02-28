import json
import os

from IndiceContribuicao import IndiceContribuicao


class IndexadorContribuicao():
    def __init__(self, pasta_prefs, pasta_hardware):
        self.pasta_prefs = pasta_prefs
        self.pasta_hardware = pasta_hardware
        pasta_pacotes = os.path.join(pasta_prefs, 'packages')
        self.indice_contribuicoes = None
        self.index = None
        pass

    def parse_index(self, path=None):
        if path is not None:
            data = json.load(open(path))
            return IndiceContribuicao(data)
        else:
            self.merge_contribuicoes(os.path.join(self.pasta_hardware, "package_index_bundled.json"))
            self.merge_contribuicoes(os.path.join(self.pasta_prefs, "package_index.json"))
            # TODO indices de 3º's

    def merge_contribuicoes(self, path):
        if not os.path.exists(path):
            return
        if self.indice_contribuicoes is None:
            self.indice_contribuicoes = self.parse_index(path)
        else:
            self.indice_contribuicoes.adicionar_pacotes(self.parse_index(path).get_pacotes_dicio())

    def get_plataforma_contribuida(self, plataforma_alvo):
        for plataforma in self.get_plataformas_instaladas():
            if plataforma.get_pasta_instalada() == plataforma_alvo.get_pasta():
                return plataforma
        return None

    def get_plataformas_instaladas(self):
        if self.index is None:
            return list()
        return self.index.get_plataformas_instaladas()
