def carregar(arquivo):
    prefs = dict()
    with open(arquivo, 'r') as linhas:
        for linha in linhas.readlines():
            if len(linha) < 2 or linha.startswith('#'):
                continue
            else:
                valores = linha.split("=")
                prefs[valores[0].strip()] = valores[1].strip()
    return prefs


def primeiro_nivel(dicio):
    opcoes = dict()
    for chave in dicio.keys():
        if chave.__contains__('.'):
            pai, filho = chave.split('.', 1)
            opcoes[pai] = dict()
            opcoes[pai][filho] = dicio[chave]
    return opcoes


def dicionario_superior(dicio):
    res = dict()
    for chave in dicio.keys():
        if not chave.__contains__('.'):
            res[chave] = dicio[chave]
    return res
