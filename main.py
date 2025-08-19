import sys
from PySide6.QtWidgets import QApplication
from app_window import RickAndMortyApp

if __name__ == "__main__":
    app = QApplication(sys.argv)
    janela = RickAndMortyApp()
    janela.show()
    sys.exit(app.exec())