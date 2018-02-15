#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
The original code is licensed under a modified BSD License
and is available at: https://wiki.python.org/moin/PyQt/Python%20syntax%20highlighting

Copyright (C) 2017  DavidBoddie

modified by: Mateus Berardo, 2018
email: mateus.berardo@brino.cc

Br.ino Qt DestaqueSintaxe

Codigo de destaque da sintaxe do BRpp da IDE Br.ino
em PyQt4 (python 2.7)

    IDE do Br.ino  Copyright (C) 2018  Br.ino

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

website: brino.cc
author: Mateus Berardo
email: mateus.berardo@brino.cc
contributor: Victor Rodrigues Pacheco
email: victor.pacheco@brino.cc
"""

from PyQt5.QtCore import QRegExp, Qt
from PyQt5.QtGui import QColor, QTextCharFormat, QFont, QSyntaxHighlighter

import GerenciadorDeKeywords


def format_(color, style=''):
    """Return a QTextCharFormat with the given attributes.
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


# Syntax styles that can be shared by all languages
STYLES = {
    'keyword': format_('#D2D200', 'bold'),
    'keyword_2': format_('#60BC0E'),
    'keyword_3': format_('#D2D200'),
    'keyword_4': format_('#A6E22E', 'bold'),
    'brace': format_('lightGray'),
    'defclass': format_('black', 'bold'),
    'string': format_('#E3ED77'),
    'string2': format_('darkMagenta'),
    'comment': format_('Gray', 'italic'),
    'self': format_('black', 'italic'),
    'numbers': format_('#52e3f6'),
}


class PythonHighlighter(QSyntaxHighlighter):
    """Syntax highlighter for the Python language.
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

        # Keyword, operator, and brace rules
        rules += [(r'\b%s\b' % w, 0, STYLES['keyword'])
                  for w in PythonHighlighter.keywords_1]
        rules += [(r'%s' % o, 0, STYLES['keyword_2'])
                  for o in PythonHighlighter.keywords_2]
        rules += [(r'%s' % b, 0, STYLES['keyword_3'])
                  for b in PythonHighlighter.keywords_3]
        rules += [(r'%s' % b, 0, STYLES['keyword_4'])
                  for b in PythonHighlighter.keywords_4]

        # All other rules
        rules += [
            # 'self'
            (r'\bself\b', 0, STYLES['self']),

            # Double-quoted string, possibly containing escape sequences
            (r'"[^"\\]*(\\.[^"\\]*)*"', 0, STYLES['string']),
            # Single-quoted string, possibly containing escape sequences
            (r"'[^'\\]*(\\.[^'\\]*)*'", 0, STYLES['string']),

            # From '//' until a newline
            (r'//[^\n]*', 0, STYLES['comment']),

            # Numeric literals
            (r'\b[+-]?[0-9]+[lL]?\b', 0, STYLES['numbers']),
            (r'\b[+-]?0[xX][0-9A-Fa-f]+[lL]?\b', 0, STYLES['numbers']),
            (r'\b[+-]?[0-9]+(?:\.[0-9]+)?(?:[eE][+-]?[0-9]+)?\b', 0, STYLES['numbers']),
        ]

        # Build a QRegExp for each pattern
        self.rules = [(QRegExp(pat), index, fmt)
                      for (pat, index, fmt) in rules]

        formato_funcao = QTextCharFormat()
        formato_funcao.setFontItalic(True)
        self.rules.append((QRegExp("\\b[A-Za-z0-9_]+(?=\\()"), 0, formato_funcao))

        self.commentStartExpression = QRegExp("/\\*")
        self.commentEndExpression = QRegExp("\\*/")
        self.multiLineCommentFormat = QTextCharFormat()
        self.multiLineCommentFormat.setForeground(Qt.cyan)

    def highlightBlock(self, texto):
        """Apply syntax highlighting to the given block of text.
        """
        # Do other syntax formatting
        for expression, nth, format_ in self.rules:
            indice = expression.indexIn(texto, 0)

            while indice >= 0:
                # We actually want the indice of the nth match
                indice = expression.pos(nth)
                length = expression.matchedLength()
                self.setFormat(indice, length, format_)
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
            indice_inicio = self.commentStartExpression.indexIn(texto, indice_inicio + comprimento_comentario);
