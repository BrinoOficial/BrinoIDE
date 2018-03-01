def carregar(arquivo):
    prefs = dict()
    with open(arquivo, 'r') as linhas:
        for linha in linhas.readlines():
            if len(linha) < 2 or linha.startswith('#'):
                continue
            else:
                valores = linha.split("=")
                adicionar = {valores[0].strip(): valores[1].strip()}
                prefs.update(adicionar)
    return prefs


def primeiro_nivel(dicio):
    opcoes = dict()
    for chave in dicio.keys():
        if chave.__contains__('.'):
            pai, filho = chave.split('.', 1)
            if opcoes.get(pai, None) is None:
                opcoes[pai] = dict()
            opcoes[pai][filho] = dicio[chave]
    return opcoes


def dicionario_superior(dicio):
    res = dict()
    for chave in dicio.keys():
        if not chave.__contains__('.'):
            res[chave] = dicio[chave]
    return res


def sub_tree(dictio, parent, sublevels=-1):
    res = dict()
    parent += "."
    parent_len = len(parent)
    for key in dictio.keys():
        if key.startswith(parent):
            nova_chave = key[parent_len:]
            key_sub_levels = len(nova_chave.split("\\."))
            if sublevels == -1 or key_sub_levels == sublevels:
                res[nova_chave] = dictio.get(key)
    return res
