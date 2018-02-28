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

    def achar_plataforma(self, arquitetura, versao):
        for plataforma in self.get_plataformas():
            if plataforma.get_arquitetura() == arquitetura and versao == plataforma.get_versao():
                return plataforma

    def achar_ferramenta(self, nome, versao):
        if self.get_ferramenta_por_nome(nome).get_versao() == versao:
            return self.get_ferramenta_por_nome(nome)
