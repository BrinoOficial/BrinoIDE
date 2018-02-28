from FerramentaContribuida import FerramentaContribuida
from PlataformaContribuida import PlataformaContribuida


class PacoteContribuido:
    def __init__(self, data):
        self.plataformas = dict()
        self.ferramentas = dict()
        self.nome = data['name']
        self.mantenedor = data['maintainer']
        for plat in data['platforms']:
            plataforma = PlataformaContribuida(plat, self)
            self.plataformas[plataforma.get_nome()] = plataforma
        for tool in data['tools']:
            ferramenta = FerramentaContribuida(tool, self)
            self.ferramentas[ferramenta.get_nome()] = ferramenta

    def get_nome(self):
        return self.nome

    def get_plataformas(self):
        return self.plataformas.values()

    def get_ferramentas(self):
        return self.ferramentas

    def get_ferramenta_por_nome(self, nome):
        return self.ferramentas[nome]
