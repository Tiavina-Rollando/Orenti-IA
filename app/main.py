import sys
from pathlib import Path

# Ajoute le dossier racine du projet (D:\Projet\Orenti'IA) au sys.path
root_dir = Path(__file__).resolve().parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))



from PySide6.QtWidgets import QApplication

from ui.main_window import MainWindow


def main():
    app = QApplication(sys.argv)

    app.setApplicationName("ORIENT'IA")
    app.setOrganizationName("ORIENT'IA")

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()