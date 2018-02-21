import os


class PlataformaAlvo:

    def __init__(self, arch, pasta, pacote_pai):
        self.id_ = arch
        self.pasta = pasta
        self.pacote_pai = pacote_pai
        arquivo_placas = os.path.join(pasta, 'boards.txt')
        if not os.path.exists(arquivo_placas):
            print "no boards.txt"
