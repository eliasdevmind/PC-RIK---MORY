from PySide6.QtCore import QObject, Signal
import requests

class Worker(QObject):
    dados_prontos = Signal(list)
    erro = Signal(str)

    def __init__(self, pagina):
        super().__init__()
        self.pagina = pagina

    def run(self):
        try:
            url = f"https://rickandmortyapi.com/api/character?page={self.pagina}"
            resposta = requests.get(url, timeout=5)
            if resposta.status_code == 200:
                dados = resposta.json()
                personagens = dados["results"]
                self.dados_prontos.emit(personagens)
            else:
                self.erro.emit("Erro ao buscar personagens.")
        except Exception as e:
            self.erro.emit(str(e))