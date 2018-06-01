"""

autor: smitkpatel
available at: https://stackoverflow.com/questions/28956693/pyqt5-qtextedit-auto-completion
modified by: Mateus Berardo
date: 13/05/2018
"""

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QCompleter

from GerenciadorDeKeywords import get_words


class MeuDicionarioComplete(QCompleter):
    insertText = pyqtSignal(str)

    def __init__(self, minhas_palavras_chaves=None, parent=None):
        minhas_palavras_chaves = get_words('1') + get_words('2') + get_words('3') + get_words('4')
        minhas_palavras_chaves = sorted(minhas_palavras_chaves)
        QCompleter.__init__(self, minhas_palavras_chaves, parent)
        self.activated.connect(self.changeCompletion)

    def changeCompletion(self, completion):
        if completion.find("(") != -1:
            completion = completion[:completion.find("(")]
        print(completion)
        self.insertText.emit(completion)
