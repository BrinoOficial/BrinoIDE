#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
import os

import MapaUtils
from IndiceContribuicao import IndiceContribuicao
from PacoteAlvo import PacoteAlvo
from PlataformaAlvo import PlataformaAlvo


class IndexadorContribuicao:
    def __init__(self, pasta_prefs, pasta_hardware):
        self.pasta_prefs = pasta_prefs
        self.pasta_hardware = pasta_hardware
        self.pasta_pacotes = os.path.join(pasta_prefs, 'packages')
        self.indice = None

    def parse_index(self, path=None):
        if path is not None:
            data = json.load(open(path))
            return IndiceContribuicao(data)
        else:
            self.merge_contribuicoes(os.path.join(self.pasta_hardware, "package_index_bundled.json"))
            self.merge_contribuicoes(os.path.join(self.pasta_prefs, "package_index.json"))
            # TODO indices de 3º's
            for plataforma in self.indice.get_plataformas():
                plataforma.resolver_dependencias_ferramentas()

    def merge_contribuicoes(self, path):
        if not os.path.exists(path):
            return
        if self.indice is None:
            self.indice = self.parse_index(path)
        else:
            self.indice.adicionar_pacotes(self.parse_index(path).get_pacotes_dicio())

    def get_plataforma_contribuida(self, plataforma_alvo):
        for plataforma in self.get_plataformas_instaladas():
            if plataforma.get_pasta_instalada() == plataforma_alvo.get_pasta():
                return plataforma
        return None

    def get_plataformas_instaladas(self):
        if self.indice is None:
            return list()
        return self.indice.get_plataformas_instaladas()

    def criar_pacotes_alvo(self):
        pacotes = list()
        for pacote in self.indice.get_pacotes():
            pacote_ = PacoteAlvo(pacote.get_nome())
            plataformas = pacote.get_plataformas()
            if plataformas:
                for plataforma in pacote.get_plataformas():
                    arq = plataforma.get_arquitetura()
                    pasta = plataforma.get_pasta_instalada()
                    plat = PlataformaAlvo(arq, pasta, pacote)
                    pacote_.adicionar_plataforma(plat)
                if pacote_.get_plataformas:
                    pacotes.append(pacote_)
        return pacotes

    def sincronizar_com_arquivos(self):
        self.sincronizar_hardware_incluido()

        self.sincronizar_pacotes_locais()

    def sincronizar_hardware_incluido(self):
        for pasta in [os.path.join(self.pasta_hardware, x) for x in os.listdir(self.pasta_hardware) if
                      os.path.isdir(os.path.join(self.pasta_hardware, x))]:
            pacote = self.indice.get_pacote(os.path.basename(pasta))
            if pacote is None:
                continue
            self.sincronizar_pacote_incluido(pacote, pasta)
            pasta_tools = os.path.join(self.pasta_hardware, 'tools')
            for pasta_ferramenta in [os.path.join(pasta_tools, x) for x in os.listdir(pasta_tools) if
                                     os.path.isdir(os.path.join(pasta_tools, x))]:
                versao_ferramentas = MapaUtils.sub_tree(
                    MapaUtils.carregar(os.path.join(pasta_ferramenta, 'builtin_tools_versions.txt')), pacote.get_nome())
                for nome in versao_ferramentas.keys():
                    self.sincronizar_ferramenta_com_sistema(pacote, pasta_ferramenta, nome,
                                                            versao_ferramentas.get(nome))

    def sincronizar_pacote_incluido(self, pacote, pasta_hardware):
        for pasta in [os.path.join(pasta_hardware, x) for x in os.listdir(pasta_hardware) if
                      os.path.isdir(os.path.join(pasta_hardware, x))]:
            versao = MapaUtils.carregar(os.path.join(pasta, "platform.txt")).get('version')
            self.sincronizar_hardware_com_arquivos(pacote, pasta, os.path.basename(pasta), versao)

    def sincronizar_hardware_com_arquivos(self, pacote, pasta, arquitetura, versao):
        plataforma = pacote.achar_plataforma(arquitetura, versao)
        plataforma.set_pasta_instalada(pasta)

    def sincronizar_ferramenta_com_sistema(self, pacote, pasta, nome, versao):
        fer = pacote.achar_ferramenta(nome, versao)
        fer.set_pasta_instalada(pasta)

    def sincronizar_pacotes_locais(self):
        if os.path.exists(self.pasta_pacotes):
            for pasta in [os.path.join(self.pasta_pacotes, x) for x in os.listdir(self.pasta_pacotes) if
                          os.path.isdir(os.path.join(self.pasta_pacotes, x))]:
                pacote = self.indice.get_pacote(os.path.basename(pasta))
                self.sincronizar_pacote_com_sistema(pacote, pasta)

    def sincronizar_pacote_com_sistema(self, pacote, pasta):
        for pasta_plataforma in [os.path.join(pasta, 'hardware', x) for x in os.listdir(os.path.join(pasta, "hardware"))
                                 if os.path.isdir(os.path.join(pasta, 'hardware', x))]:
            for pasta_versao in [os.path.join(pasta_plataforma, x) for x in os.listdir(pasta_plataforma) if
                                 os.path.isdir(os.path.join(pasta_plataforma, x))]:
                self.sincronizar_hardware_com_arquivos(pacote, pasta_versao, os.path.basename(pasta_plataforma),
                                                       os.path.basename(pasta_versao))
        for pasta_ferramenta in [os.path.join(pasta, 'tools', x) for x in os.listdir(os.path.join(pasta, 'tools')) if
                                 os.path.isdir(os.path.join(pasta, 'tools', x))]:
            for versao in [os.path.join(pasta_ferramenta, x) for x in os.listdir(pasta_ferramenta) if
                           os.path.isdir(os.path.join(pasta_ferramenta, x))]:
                self.sincronizar_ferramenta_com_sistema(pacote, versao, os.path.basename(pasta_ferramenta),
                                                        os.path.basename(versao))
