import sys
from pathlib import Path
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap  # <-- AJOUT ICI
from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QPushButton,
    QLabel,
    QStackedWidget,
    QFrame,
)
from ui.home_page import HomePage
from ui.profile_page import ProfilePage
from ui.recommandation_page import RecommendationPage
from ui.chat_page import ChatPage

def get_resource_path(relative_path: str) -> Path:
    """ Résout le chemin d'accès compatible Dev et PyInstaller (.exe) """
    if hasattr(sys, "_MEIPASS"):
        return Path(sys._MEIPASS) / relative_path
    
    # Recherche à partir du fichier actuel (ui/main_window.py -> racine du projet)
    base_dir = Path(__file__).resolve().parent.parent.parent
    path = base_dir / relative_path
    
    if not path.exists():
        # Tentative depuis le répertoire de travail courant (D:\Projet\Orenti'IA)
        path = Path.cwd() / relative_path

    return path

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("ORIENT'IA - Assistant d'orientation")
        self.resize(1200, 750)

        self.setup_ui()
        self.apply_style()
    
    def setup_ui(self):

        # =====================================================
        # WIDGET CENTRAL
        # =====================================================

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # =====================================================
        # MENU GAUCHE
        # =====================================================

        sidebar = QFrame()
        sidebar.setObjectName("sidebar")
        sidebar.setFixedWidth(240)

        # On met 0 marge à gauche/droite du sidebar pour que le bloc blanc touche les bords
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(0, 20, 0, 20)
        sidebar_layout.setSpacing(10)

        # Helper pour ajouter du padding interne aux autres éléments du menu
        def add_padded_widget(widget, padding_horizontal=15):
            container = QWidget()
            layout = QHBoxLayout(container)
            layout.setContentsMargins(padding_horizontal, 0, padding_horizontal, 0)
            layout.addWidget(widget)
            return container

        # Logo / titre
        title = QLabel("ORIENT'IA")
        title.setObjectName("logo")

        subtitle = QLabel("Assistant d'orientation")
        subtitle.setObjectName("subtitle")

        sidebar_layout.addWidget(add_padded_widget(title))
        sidebar_layout.addWidget(add_padded_widget(subtitle))

        sidebar_layout.addSpacing(30)

        # =====================================================
        # BOUTONS
        # =====================================================

        self.btn_home = self.create_menu_button("🏠  Accueil")
        self.btn_profile = self.create_menu_button("👤  Mon profil")
        self.btn_recommendation = self.create_menu_button("🎯  Recommandations")
        self.btn_chat = self.create_menu_button("💬  Assistant IA")

        sidebar_layout.addWidget(add_padded_widget(self.btn_home))
        sidebar_layout.addWidget(add_padded_widget(self.btn_profile))
        sidebar_layout.addWidget(add_padded_widget(self.btn_recommendation))
        sidebar_layout.addWidget(add_padded_widget(self.btn_chat))

        sidebar_layout.addStretch()

        # =====================================================
        # LOGO UNIVERSITÉ (PLEINE LARGEUR 240px)
        # =====================================================
        logo_container = QFrame()
        logo_container.setObjectName("logoContainer")
        
        logo_container_layout = QVBoxLayout(logo_container)
        # Marges haut/bas de 10px, 0px sur les côtés pour occuper toute la largeur
        logo_container_layout.setContentsMargins(0, 10, 0, 10)

        logo_label = QLabel()
        logo_label.setAlignment(Qt.AlignCenter)
        
        logo_path = get_resource_path("assets/logo_ispm.png")
        if logo_path.exists():
            pixmap = QPixmap(str(logo_path))
            if not pixmap.isNull():
                # On ajuste l'image à la largeur exacte du sidebar (240px)
                scaled_pixmap = pixmap.scaledToWidth(240, Qt.SmoothTransformation)
                logo_label.setPixmap(scaled_pixmap)

        logo_container_layout.addWidget(logo_label)
        
        sidebar_layout.addWidget(logo_container)
        sidebar_layout.addSpacing(15)

        # Mode offline
        offline = QLabel("●  Mode hors ligne")
        offline.setObjectName("offline")

        sidebar_layout.addWidget(add_padded_widget(offline))
        
        # =====================================================
        # ZONE DES PAGES
        # =====================================================

        self.pages = QStackedWidget()

        self.home_page = HomePage()
        self.profile_page = ProfilePage()
        self.recommendation_page = RecommendationPage()
        self.chat_page = ChatPage()

        self.pages.addWidget(self.home_page)
        self.pages.addWidget(self.profile_page)
        self.pages.addWidget(self.recommendation_page)
        self.pages.addWidget(self.chat_page)

        # =====================================================
        # ASSEMBLAGE
        # =====================================================

        main_layout.addWidget(sidebar)
        main_layout.addWidget(self.pages)

        # =====================================================
        # CONNECTIONS
        # =====================================================

        self.btn_home.clicked.connect(
            lambda: self.change_page(0)
        )

        self.btn_profile.clicked.connect(
            lambda: self.change_page(1)
        )

        self.btn_recommendation.clicked.connect(
            lambda: self.change_page(2)
        )

        self.btn_chat.clicked.connect(
            lambda: self.change_page(3)
        )

        self.change_page(0)

    def create_menu_button(self, text):

        button = QPushButton(text)
        button.setObjectName("menuButton")
        button.setCursor(Qt.PointingHandCursor)

        return button

    def change_page(self, index):

        self.pages.setCurrentIndex(index)

        buttons = [
            self.btn_home,
            self.btn_profile,
            self.btn_recommendation,
            self.btn_chat,
        ]

        for button in buttons:
            button.setProperty("active", False)

            button.style().unpolish(button)
            button.style().polish(button)

        buttons[index].setProperty("active", True)

        buttons[index].style().unpolish(buttons[index])
        buttons[index].style().polish(buttons[index])

    def apply_style(self):

        self.setStyleSheet("""

            QMessageBox {
                background-color: #172033;
                color: white;
            }

            QMessageBox QLabel {
                color: white;
            }

            QMessageBox QPushButton {
                background-color: #315efb;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 8px 18px;
                min-width: 70px;
            }

            QMessageBox QPushButton:hover {
                background-color: #244bd0;
            }
            
            QMainWindow {
                background-color: #f5f7fb;
            }

            QWidget {
                color: #172033;
            }

            QLabel {
                color: #172033;
            }

            QLineEdit {
                color: #172033;
                background-color: white;
            }

            QComboBox {
                color: #172033;
                background-color: white;
            }

            QTextEdit {
                color: #172033;
                background-color: white;
            }

            QPushButton {
                color: #172033;
            }

            #sidebar {
                background-color: #172033;
            }

            #logo {
                color: white;
                font-size: 24px;
                font-weight: bold;
            }

            #subtitle {
                color: #aab4c8;
                font-size: 12px;
            }

            #menuButton {
                color: #dce3ef;
                background-color: transparent;
                border: none;
                padding: 14px;
                text-align: left;
                border-radius: 8px;
                font-size: 14px;
            }

            #menuButton:hover {
                background-color: #263550;
            }

            #menuButton[active="true"] {
                background-color: #315efb;
                color: white;
                font-weight: bold;
            }

            #offline {
                color: #78d68f;
                padding: 8px;
                font-size: 12px;
            }

            QLabel#pageTitle {
                color: #172033;
                font-size: 28px;
                font-weight: bold;
            }

            QLabel#pageSubtitle {
                color: #687386;
                font-size: 14px;
            }

            QLineEdit,
            QComboBox,
            QTextEdit,
            QSpinBox {
                border: 1px solid #d6dce7;
                border-radius: 6px;
                padding: 8px;
                background: white;
                color: #172033;
            }

            QPushButton#primaryButton {
                background-color: #315efb;
                color: white;
                border: none;
                border-radius: 7px;
                padding: 10px 18px;
                font-weight: bold;
            }

            QPushButton#primaryButton:hover {
                background-color: #244bd0;
            }

            QFrame#card {
                background-color: white;
                border: 1px solid #e1e6ef;
                border-radius: 10px;
            }
        """)