class PlataformaContribuida:
    def __init__(self, data, parent):
        self.nome = data['name']
        self.pacote = parent
        self.arq = data['architecture']
        self.versao = data['version']
        self.categoria = data['category']
        self.placas = data['boards']
        self.ferramentas = data['toolsDependencies']
        self.ferramentas_resolvidas = dict()
        self.pasta_instalada = ""

    def get_ferramentas_resolvidas(self):
        return self.ferramentas_resolvidas.values()

    def resolver_dependencias_ferramentas(self):
        for tool in self.ferramentas:
            self.ferramentas_resolvidas[tool['name']] = self.pacote.get_ferramenta_por_nome(tool['name'])

    def get_pasta_instalada(self):
        return self.pasta_instalada

    def get_arquitetura(self):
        return self.arq

    def get_versao(self):
        return self.versao

    def set_pasta_instalada(self, pasta):
        self.pasta_instalada = pasta

    def get_nome(self):
        return self.nome
