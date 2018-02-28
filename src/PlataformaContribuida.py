class PlataformaContribuida:
    def __init__(self, data):
        self.nome = data['name']
        self.arq = data['architecture']
        self.categoria = data['category']
        self.placas = data['boards']

    def get_ferramentas_resolvidas(self):
        return self.referencias_ferramentas_resolvidas.values()
