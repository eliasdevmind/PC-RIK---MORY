from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt
import requests

class DetalhesPersonagemDialog(QDialog):
    def __init__(self, personagem, parent=None):
        super().__init__(parent)
        self.setWindowTitle(personagem["name"])
        self.setMinimumWidth(300)

        layout = QVBoxLayout()

        try:
            img_data = requests.get(personagem["image"], timeout=5).content
            pixmap = QPixmap()
            pixmap.loadFromData(img_data)
            imagem_label = QLabel()
            imagem_label.setPixmap(pixmap.scaled(200, 200, Qt.KeepAspectRatio))
            imagem_label.setAlignment(Qt.AlignCenter)
            layout.addWidget(imagem_label)
        except:
            pass

        info = [
            f"🧠 Nome: {personagem['name']}",
            f"📍 Status: {personagem['status']}",
            f"🧬 Espécie: {personagem['species']}",
            f"⚧ Gênero: {personagem['gender']}",
            f"🌍 Origem: {personagem['origin']['name']}",
            f"🎬 Episódios: {len(personagem['episode'])}"
        ]

        for linha in info:
            label = QLabel(linha)
            layout.addWidget(label)

        self.setLayout(layout)