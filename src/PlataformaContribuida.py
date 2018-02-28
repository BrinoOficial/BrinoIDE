class PlataformaContribuida:
    def __init__(self, data, parent):
        self.nome = data['name']
        self.pacote = parent
        self.arq = data['architecture']
        self.categoria = data['category']
        self.placas = data['boards']
        self.ferramentas = data['toolsDependencies']
        self.ferramentas_resolvidas = dict()

    def get_ferramentas_resolvidas(self):
        return self.referencias_ferramentas_resolvidas.values()

    def resolver_dependencias_ferramentas(self):
        for tool in self.ferramentas:
            self.ferramentas_resolvidas[tool['name']] = self.pacote.get_ferramenta_por_nome(tool['name'])
