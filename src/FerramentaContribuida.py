class FerramentaContribuida:
    def __init__(self, data):
        self.nome = data['name']
        self.versao = data['version']
        self.sistemas = dict()

    def get_nome(self):
        return self.nome
