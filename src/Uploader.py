import Preferencias


def novo_uploader(placa_alvo, porta, nao_existe_porta):
    if nao_existe_porta:
        return UploaderSerial(nao_existe_porta)
    if porta is not None and porta.get_protocolo() == "network":
        if porta.get_prefs().get("ssh_upload") == "no":
            pass
            # TODO Network Uploader
        # TODO SSH Uploader


def get_uploader_por_preferencias():
    # TODO
    pass


class UploaderSerial():
    def __init__(self, nao_existe_porta=False):
        self.verbose = Preferencias.get("upload.verbose")
        self.verificar_carregar = Preferencias.get("upload.verify")
        self.error = ""
        self.erro_nao_encontrado = False
        self.nao_existe_porta = nao_existe_porta

    # sucesso = Uploader.upload_usando_preferencias(self, caminho, caminho_temp, nome, usando_programador)

    def upload_usando_preferencias(self, parent, caminho_temp, nome):
        plataforma_alvo = parent.get_plataforma_alvo()
        prefs = Preferencias.get_mapa()
        preferencias_placa = parent.get_preferencias_placa()
        print preferencias_placa
        if preferencias_placa is not None:
            prefs.update(preferencias_placa)
        tool = prefs["upload.tool"]
        if tool.__contains__(":"):
            separado = tool.split(":", 2)
            plataforma_alvo = parent.get_plataforma_alvo_do_pacote(separado[0])
            tool = separado[1]
        prefs.update(plataforma_alvo.get_ferramenta(tool))
        # TODO upload com programador
        if self.nao_existe_porta:
            prefs["build.path"] = caminho_temp
            prefs["build.project_name"] = nome
            # TODO upload verify
            resultado = False
            padrao = prefs.get("upload.pattern")
            cmd = formatar_e_dividir(padrao, prefs, True)
            print cmd


def formatar_e_dividir(src, dictio, recursivo):
    res = ""
    for i in range(10):
        res = substituir_do_mapa(src, dictio)
        if not recursivo:
            break
        if res == src:
            break
        src = res
    return separacao_quotes(src, '"\'', False)


def substituir_do_mapa(src, dictio, delimitador_esquerdo='{', delimitador_direito='}'):
    for key in dictio.keys():
        keyword = delimitador_esquerdo + key + delimitador_direito
        if dictio.get(key) is not None and keyword is not None:
            src = src.replace(keyword, dictio.get(key))
    return src


def separacao_quotes(src, quote_chars, arg_vazios):
    res = list()
    arg_escapado = None
    char_escapador = None
    for s in src.split(" "):
        if char_escapador is None:
            first = None
            if len(s) > 0:
                first = s[0:1]
            if first is None or not quote_chars.__contains__(first):
                if not len(s.strip()) == 0 or arg_vazios:
                    res.append(s)
                continue
            char_escapador = first
            s = s[1:]
            arg_escapado = ""
        if not s.endswith(char_escapador):
            arg_escapado += s + " ";
            continue
        arg_escapado += s[0:len(s) - 1]
        if not len(arg_escapado.strip()) == 0 or arg_vazios:
            res.append(arg_escapado)
            char_escapador = None
    if char_escapador is not None:
        print("Erro")
    return res
