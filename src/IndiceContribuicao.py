from PacoteContribuido import PacoteContribuido


class IndiceContribuicao:
    def __init__(self, data=None):
        self.pacotes = dict()
        if data is not None:
            for package in data['packages']:
                pacote = PacoteContribuido(package)
                self.pacotes[pacote.get_nome()] = pacote

    def get_plataformas_instaladas(self):
        return self.get_plataformas()

    def get_plataformas(self):
        plataformas = list()
        pacs = self.get_pacotes()
        for pacote in pacs:
            for plataforma in pacote.get_plataformas():
                plataformas.append(plataforma)
        return plataformas

    def get_pacotes(self):
        return self.pacotes.values()

    def adicionar_pacotes(self, dicio):
        self.pacotes.update(dicio)

    def get_pacotes_dicio(self):
        return self.pacotes

    def get_pacote(self, nome):
        print "Nome:", nome
        print self.get_pacotes_dicio().get(nome)
        return self.get_pacotes_dicio().get(nome)
