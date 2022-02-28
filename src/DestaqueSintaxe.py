#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Br.ino - BotaoImagem

Reaiza o destaque dos termos brino e arduino

    IDE do Br.ino  Copyright (C) 2022  Br.ino

    Este arquivo e parte da IDE do Br.ino.

    A IDE do Br.ino e um software livre: voce pode redistribui-lo
    e / ou modifica-lo de acordo com os termos da Licenca Publica
    Geral GNU, conforme publicado pela Free Software Foundation,
    seja a versao 3 da Licenca , ou (na sua opcao) qualquer
    versao posterior.

    A IDE do Br.ino e distribuida na esperanca de que seja util,
    mas SEM QUALQUER GARANTIA; sem a garantia implicita de
    COMERCIALIZACAO ou ADEQUACAO A UM DETERMINADO PROPOSITO.
    Consulte a Licenca Publica Geral GNU para obter mais detalhes.

    Voce deveria ter recebido uma copia da Licenca Publica Geral
    GNU junto com este programa. Caso contrario, veja
    <https://www.gnu.org/licenses/>

site: https://brino.cc
codigo completo disponivel em https://github.com/BrinoOficial/BrinoIDE
autor: Victor Rodrigues Pacheco
autor: Gabriel Rodrigues Pacheco
autor: Mateus Berardo
"""

from PyQt5.QtCore import QRegExp, Qt
from PyQt5.QtGui import QColor, QTextCharFormat, QFont, QSyntaxHighlighter

import GerenciadorDeKeywords


def format_(color, style=''):
    """
    Retorna a formatacao da palavra a ser destacada
    :param color:
        Cor da palavra
    :param style:
        Estilo da palavra
    :return:
        Formato
    """
    _color = QColor()
    _color.setNamedColor(color)

    _format = QTextCharFormat()
    _format.setForeground(_color)
    if 'bold' in style:
        _format.setFontWeight(QFont.Bold)
    if 'italic' in style:
        _format.setFontItalic(True)

    return _format


# Define os estilos
STYLES = {
    'keyword': format_('#D2D200', 'bold'),
    'keyword_2': format_('#60BC0E'),
    'keyword_3': format_('#D2D200'),
    'keyword_4': format_('#A6E22E', 'bold'),
    'brace': format_('lightGray'),
    'defclass': format_('black', 'bold'),
    'string': format_('#E3ED77'),
    'comment': format_('Gray', 'italic'),
    'numbers': format_('#52e3f6'),
    'function': format_('#efefef', 'italic')
}


class PythonHighlighter(QSyntaxHighlighter):
    """
    Define os devidos hightlightes de cada uma das categorias de keyword do arduino e do brino
    """
    # Br.ino keywords tipo 1
    keywords_1 = GerenciadorDeKeywords.get_highlights('1')

    # Br.ino keywords tipo 2
    keywords_2 = GerenciadorDeKeywords.get_highlights('2')

    # Br.ino keywords tipo 3
    keywords_3 = GerenciadorDeKeywords.get_highlights('3')

    # Br.ino keywords tipo 4
    keywords_4 = GerenciadorDeKeywords.get_highlights('4')

    def __init__(self, document):

        QSyntaxHighlighter.__init__(self, document)
        self.parent = document

        rules = []

        rules += [(r'\\b[A-Za-z0-9_]+(?=\\()', 0, STYLES['function'])]

        # Keyword, operator, and brace rules
        rules += [(r'\b%s\b' % w, 0, STYLES['keyword'])
                  for w in PythonHighlighter.keywords_1]
        rules += [(r'%s' % o, 0, STYLES['keyword_2'])
                  for o in PythonHighlighter.keywords_2]
        rules += [(r'%s' % b, 0, STYLES['keyword_3'])
                  for b in PythonHighlighter.keywords_3]
        rules += [(r'%s' % b, 0, STYLES['keyword_4'])
                  for b in PythonHighlighter.keywords_4]

        # Todas as outras regras
        rules += [

            # string de aspas duplas
            (r'"[^"\\]*(\\.[^"\\]*)*"', 0, STYLES['string']),
            # string de aspas simples
            (r"'[^'\\]*(\\.[^'\\]*)*'", 0, STYLES['string']),

            # // ate o fim da linha (Comentario)
            (r'//[^\n]*', 0, STYLES['comment']),

            # Numerico
            (r'\b[+-]?[0-9]+[lL]?\b', 0, STYLES['numbers']),
            (r'\b[+-]?0[xX][0-9A-Fa-f]+[lL]?\b', 0, STYLES['numbers']),
            (r'\b[+-]?[0-9]+(?:\.[0-9]+)?(?:[eE][+-]?[0-9]+)?\b', 0, STYLES['numbers']),
        ]

        # Cria um QRegExp para cada expressao
        self.rules = [(QRegExp(pat), index, fmt)
                      for (pat, index, fmt) in rules]

        self.commentStartExpression = QRegExp("/\\*")
        self.commentEndExpression = QRegExp("\\*/")
        self.multiLineCommentFormat = QTextCharFormat()
        self.multiLineCommentFormat.setForeground(Qt.cyan)

    def highlightBlock(self, texto):
        """
        Aplica hightlight em dados blocos de texto
        :param texto:
            Texto a receber o hightlight
        :return:
            None
        """
        for expression, nth, formato in self.rules:
            indice = expression.indexIn(texto, 0)

            while indice >= 0:
                # We actually want the indice of the nth match
                indice = expression.pos(nth)
                length = expression.matchedLength()
                self.setFormat(indice, length, formato)
                indice = expression.indexIn(texto, indice + length)

        self.setCurrentBlockState(0)

        indice_inicio = 0

        if self.previousBlockState() != 1:
            indice_inicio = self.commentStartExpression.indexIn(texto)

        while indice_inicio >= 0:
            indice_final = self.commentEndExpression.indexIn(texto, indice_inicio)

            if indice_final == -1:
                self.setCurrentBlockState(1)
                comprimento_comentario = len(texto) - indice_inicio
            else:
                comprimento_comentario = indice_final - indice_inicio + self.commentEndExpression.matchedLength()

            self.setFormat(indice_inicio, comprimento_comentario,
                           self.multiLineCommentFormat)
            indice_inicio = self.commentStartExpression.indexIn(texto, indice_inicio + comprimento_comentario)
