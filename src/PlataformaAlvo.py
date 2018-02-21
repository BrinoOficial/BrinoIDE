import os


class PlataformaAlvo:

    def __init__(self, arch, pasta, pacote_pai):
        self.id_ = arch
        self.pasta = pasta
        self.pacote_pai = pacote_pai

        arquivo_placas = os.path.join(pasta, 'boards.txt')
        if not os.path.exists(arquivo_placas):
            print "no boards.txt"
        preferencias_placas = self.carregar(arquivo_placas)
        self.preferencias = self.carregar(os.path.join(pasta, 'platform.txt'))
        # TODO preferencias LegacyTargetPlatform

    def carregar(self, arquivo):
        prefs = dict()
        with open(arquivo, 'r') as linhas:
            for linha in linhas.readlines():
                if len(linha) < 2 or linha.startswith('#'):
                    continue
                else:
                    valores = linha.split("=")
                    prefs[valores[0].strip()] = valores[1].strip()
        return prefs

    def get_preferencias(self):
        return self.preferencias
