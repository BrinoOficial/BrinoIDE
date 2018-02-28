class FerramentaContribuida:
    def __init__(self, data, pacote_pai=None):
        self.pacote = pacote_pai
        self.nome = data['name']
        self.versao = data['version']
        self.sistemas = dict()
        self.pasta_instalada = ""

    def get_nome(self):
        return self.nome

    def get_versao(self):
        return self.versao

    def set_pasta_instalada(self, pasta):
        self.pasta_instalada = pasta

    def get_pasta_instalada(self):
        return self.pasta_instalada
