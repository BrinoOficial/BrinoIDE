from PacoteContribuido import PacoteContribuido


class IndiceContribuicao:
    def __init__(self, data=None):
        self.pacotes = dict()
        if data is not None:
            for package in data['packages']:
                pacote = PacoteContribuido(package)
                self.pacotes[pacote.get_nome()] = pacote

    def get_plataformas_instaladas(self):
        pass

    def get_plataformas(self):
        pass

    def get_pacotes(self):
        pass
