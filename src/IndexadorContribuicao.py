class IndexadorContribuicao():
    def __init__(self):
        self.index = None
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
