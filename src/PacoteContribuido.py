from FerramentaContribuida import FerramentaContribuida
from PlataformaContribuida import PlataformaContribuida


class PacoteContribuido:
    def __init__(self, data):
        self.plataformas = dict()
        self.ferramentas = dict()
        self.nome = data['name']
        self.mantenedor = data['maintainer']
        for plat in data['platforms']:
            plataforma = PlataformaContribuida(plat)
            self.plataformas[plataforma.get_nome()] = plataforma
        for tool in data['tools']:
            ferramenta = FerramentaContribuida(tool)
            self.ferramentas[ferramenta.get_nome()] = ferramenta

    def get_nome(self):
        return self.nome
