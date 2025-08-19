from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QScrollArea, QGridLayout
)
from PySide6.QtGui import QPixmap, QCursor
from PySide6.QtCore import Qt, QThread
from api_worker import Worker
from image_loader import ImageLoaderWorker
from personagem_dialog import DetalhesPersonagemDialog

class RickAndMortyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Rick and Morty - Personagens")
        self.setGeometry(100, 100, 800, 600)
        self.pagina_atual = 1
        self.image_threads = []

        self.layout_principal = QVBoxLayout(self)

        botoes_layout = QHBoxLayout()
        self.botao_anterior = QPushButton("◀ Anterior")
        self.botao_anterior.clicked.connect(self.pagina_anterior)
        self.botao_proximo = QPushButton("Próximo ▶")
        self.botao_proximo.clicked.connect(self.proxima_pagina)
        self.label_pagina = QLabel(f"Página: {self.pagina_atual}")
        self.label_pagina.setAlignment(Qt.AlignCenter)

        botoes_layout.addWidget(self.botao_anterior)
        botoes_layout.addWidget(self.label_pagina)
        botoes_layout.addWidget(self.botao_proximo)
        self.layout_principal.addLayout(botoes_layout)

        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.layout_principal.addWidget(self.scroll)

        self.container = QWidget()
        self.grid_layout = QGridLayout(self.container)
        self.grid_layout.setSpacing(15)
        self.scroll.setWidget(self.container)

        self.loading_label = QLabel("Buscando personagens...")
        self.loading_label.setAlignment(Qt.AlignCenter)
        self.layout_principal.addWidget(self.loading_label)
        self.loading_label.hide()

        self.carregar_personagens()

    def carregar_personagens(self):
        self.loading_label.show()
        self.botao_anterior.setEnabled(False)
        self.botao_proximo.setEnabled(False)

        while self.grid_layout.count():
            widget = self.grid_layout.takeAt(0).widget()
            if widget:
                widget.deleteLater()

        self.image_threads.clear()

        self.thread = QThread()
        self.worker = Worker(self.pagina_atual)
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.run)
        self.worker.dados_prontos.connect(self.mostrar_personagens)
        self.worker.erro.connect(self.mostrar_erro)
        self.worker.dados_prontos.connect(self.thread.quit)
        self.worker.erro.connect(self.thread.quit)
        self.thread.start()

    def mostrar_personagens(self, personagens):
        self.loading_label.hide()
        self.botao_anterior.setEnabled(True)
        self.botao_proximo.setEnabled(True)

        for i, personagem in enumerate(personagens):
            card = self.criar_card_personagem(personagem)
            self.grid_layout.addWidget(card, i // 3, i % 3)

        self.label_pagina.setText(f"Página: {self.pagina_atual}")

    def mostrar_erro(self, mensagem):
        self.loading_label.setText(f"Erro: {mensagem}")
        self.botao_anterior.setEnabled(True)
        self.botao_proximo.setEnabled(True)

    def criar_card_personagem(self, personagem):
        from PySide6.QtWidgets import QWidget, QVBoxLayout

        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setAlignment(Qt.AlignCenter)

        imagem_label = QLabel("Carregando...")
        imagem_label.setFixedSize(150, 150)
        imagem_label.setAlignment(Qt.AlignCenter)
        imagem_label.setCursor(QCursor(Qt.PointingHandCursor))
        imagem_label.mousePressEvent = lambda e: self.abrir_detalhes(personagem)
        layout.addWidget(imagem_label)

        img_thread = QThread()
        img_worker = ImageLoaderWorker(personagem["image"], imagem_label)
        img_worker.moveToThread(img_thread)
        img_thread.started.connect(img_worker.run)
        img_worker.imagem_carregada.connect(self.atualizar_imagem)
        img_worker.imagem_carregada.connect(img_thread.quit)
        self.image_threads.append((img_thread, img_worker))
        img_thread.start()

        nome_label = QLabel(personagem["name"])
        nome_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(nome_label)

        return widget

    def atualizar_imagem(self, pixmap, label):
        label.setPixmap(pixmap.scaled(150, 150, Qt.KeepAspectRatio))
        label.setText("")

    def abrir_detalhes(self, personagem):
        dialogo = DetalhesPersonagemDialog(personagem, self)
        dialogo.exec()

    def proxima_pagina(self):
        self.pagina_atual += 1
        self.carregar_personagens()

    def pagina_anterior(self):
        if self.pagina_atual > 1:
            self.pagina_atual -= 1
            self.carregar_personagens()