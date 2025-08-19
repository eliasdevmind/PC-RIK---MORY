from PySide6.QtCore import QObject, Signal
from PySide6.QtGui import QPixmap
import requests

class ImageLoaderWorker(QObject):
    imagem_carregada = Signal(QPixmap, object)

    def __init__(self, url, label_destino):
        super().__init__()
        self.url = url
        self.label_destino = label_destino

    def run(self):
        try:
            resposta = requests.get(self.url, timeout=5)
            if resposta.status_code == 200:
                pixmap = QPixmap()
                pixmap.loadFromData(resposta.content)
                self.imagem_carregada.emit(pixmap, self.label_destino)
        except:
            pass