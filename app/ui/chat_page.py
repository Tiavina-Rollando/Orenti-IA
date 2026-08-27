from PySide6.QtCore import Qt, QThread, Signal
from PySide6.QtWidgets import (
    QHBoxLayout,
    QLineEdit,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
    QLabel,
)

from agent.agent import ask_agent


# Thread séparé pour ne pas geler l'interface graphique durant la génération
class WorkerThread(QThread):
    finished = Signal(dict)

    def __init__(self, question):
        super().__init__()
        self.question = question

    def run(self):
        result = ask_agent(self.question)
        self.finished.emit(result)


class ChatPage(QWidget):

    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 35, 40, 35)

        title = QLabel("Assistant ORIENT'IA")
        title.setObjectName("pageTitle")

        subtitle = QLabel("Posez une question concernant votre orientation.")
        subtitle.setObjectName("pageSubtitle")

        layout.addWidget(title)
        layout.addWidget(subtitle)

        # HISTORIQUE CHAT
        self.chat = QTextEdit()
        self.chat.setReadOnly(True)
        self.chat.setStyleSheet("""
            QTextEdit {
                background-color: white;
                border: 1px solid #d6dce7;
                border-radius: 8px;
                padding: 15px;
                font-size: 13px;
            }
        """)

        self.chat.setHtml(
            "<b>ORIENT'IA :</b> Bonjour ! 👋<br>"
            "Je peux vous aider dans votre choix de formation à l'ISPM.<br><br>"
            "Posez-moi une question (ex: <i>Quels sont les prérequis pour IGGLIA ?</i> ou <i>Comparer IGGLIA et ESIIA</i>)."
        )

        layout.addWidget(self.chat)

        # SAISIE
        bottom = QHBoxLayout()

        self.input = QLineEdit()
        self.input.setPlaceholderText("Écrivez votre question...")

        self.send_button = QPushButton("Envoyer")
        self.send_button.setObjectName("primaryButton")

        self.send_button.clicked.connect(self.send_message)
        self.input.returnPressed.connect(self.send_message)

        bottom.addWidget(self.input)
        bottom.addWidget(self.send_button)

        layout.addLayout(bottom)

        # AVERTISSEMENT / DISCLAIMER (Exigence Jury)
        disclaimer = QLabel(
            "💡 <i>ORIENT'IA constitue un outil d'aide à l’orientation. "
            "Ses réponses sont fournies à titre indicatif et ne remplacent pas les décisions officielles du jury d'admission.</i>"
        )
        disclaimer.setWordWrap(True)
        disclaimer.setAlignment(Qt.AlignmentFlag.AlignCenter)
        disclaimer.setStyleSheet("color: #6c757d; font-size: 11px; margin-top: 8px;")
        
        layout.addWidget(disclaimer)

    def send_message(self):
        question = self.input.text().strip()

        if not question:
            return

        # Desactiver les entrées pendant le traitement
        self.input.clear()
        self.input.setEnabled(False)
        self.send_button.setEnabled(False)

        # Affichage du message utilisateur
        self.chat.append(f"<br><b>Vous :</b> {question}")
        self.chat.append("<br><i>ORIENT'IA est en train de réfléchir...</i>")

        # Lancement du traitement en arrière-plan
        self.worker = WorkerThread(question)
        self.worker.finished.connect(self.on_response_received)
        self.worker.start()

    def on_response_received(self, result):
        # Suppression du message de chargement (supprime la dernière ligne)
        cursor = self.chat.textCursor()
        cursor.movePosition(cursor.MoveOperation.End)
        cursor.select(cursor.SelectionType.BlockUnderCursor)
        cursor.removeSelectedText()

        answer = result.get("answer", "")
        formatted_answer = answer.replace("\n", "<br>").replace("**", "<b>").replace("**", "</b>")

        self.chat.append(f"<br><b>ORIENT'IA :</b><br>{formatted_answer}")

        sources = result.get("sources", [])
        if sources:
            sources_str = ", ".join(sources)
            self.chat.append(f"<br><small><b>Formations consultées :</b> {sources_str}</small>")

        # Réactiver la saisie
        self.input.setEnabled(True)
        self.send_button.setEnabled(True)
        self.input.setFocus()

        # Défilement automatique
        scrollbar = self.chat.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())