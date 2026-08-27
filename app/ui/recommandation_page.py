from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QPushButton,
    QLabel,
    QScrollArea,
    QFrame,
    QMessageBox,
)

from data.loader import load_profile
from ml.recommender import generate_recommendations


class RecommendationPage(QWidget):

    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 35, 40, 35)

        # -----------------------------------------------------
        # TITRE & EN-TÊTE
        # -----------------------------------------------------
        title = QLabel("Mes recommandations")
        title.setObjectName("pageTitle")

        subtitle = QLabel(
            "Les parcours d'études et formations les plus adaptés à votre profil."
        )
        subtitle.setObjectName("pageSubtitle")
        subtitle.setWordWrap(True)

        layout.addWidget(title)
        layout.addWidget(subtitle)

        # -----------------------------------------------------
        # BOUTON D'ACTION
        # -----------------------------------------------------
        self.analyze_button = QPushButton("🎯 Analyser mon profil")
        self.analyze_button.setObjectName("primaryButton")
        self.analyze_button.clicked.connect(self.run_analysis)

        layout.addWidget(self.analyze_button)

        # -----------------------------------------------------
        # ZONE SCROLLABLE POUR LES RÉSULTATS
        # -----------------------------------------------------
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setFrameShape(QScrollArea.NoFrame)

        self.container = QWidget()
        self.results_layout = QVBoxLayout(self.container)
        self.results_layout.setSpacing(15)

        self.scroll.setWidget(self.container)
        layout.addWidget(self.scroll)

        # Style complémentaire spécifique pour les cartes
        self.setStyleSheet("""
            QFrame#card {
                background-color: #ffffff;
                border: 1px solid #d1d5db;
                border-radius: 8px;
                padding: 15px;
            }
            QLabel {
                color: #1f2937;
            }
        """)

    def clear_results(self):
        """Efface les widgets de recommandations précédents."""
        while self.results_layout.count():
            item = self.results_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

    def run_analysis(self):
        """Charge le profil sauvegardé et affiche les recommandations ML."""
        self.clear_results()

        profile = load_profile()

        # Vérification si le profil existe
        if not profile:
            QMessageBox.warning(
                self,
                "Profil non renseigné",
                "Veuillez d'abord remplir et enregistrer votre profil dans l'onglet 'Mon profil'."
            )
            return

        # Génération des recommandations via le moteur ML
        try:
            result_container = generate_recommendations(profile, top_k=5)
            # Gestion selon la structure retournée (RecommendationResult ou Liste)
            recommendations = getattr(result_container, 'recommendations', result_container)
        except Exception as e:
            QMessageBox.critical(
                self,
                "Erreur d'analyse",
                f"Une erreur est survenue lors de l'analyse ML :\n{e}"
            )
            return

        if not recommendations:
            no_rec_label = QLabel("Aucune recommandation disponible pour le moment.")
            no_rec_label.setStyleSheet("color: #687386; font-size: 14px;")
            self.results_layout.addWidget(no_rec_label)
            return

        # -----------------------------------------------------
        # AFFICHAGE DES CARTES DE RECOMMANDATION
        # -----------------------------------------------------
        for index, rec in enumerate(recommendations, start=1):
            card = QFrame()
            card.setObjectName("card")

            card_layout = QVBoxLayout(card)
            card_layout.setSpacing(8)

            # Nom du parcours
            name = QLabel(f"#{index}  Parcours : {rec.parcours}")
            name.setStyleSheet("font-size: 18px; font-weight: bold; color: #1e40af;")

            # Score de compatibilité en pourcentage
            percentage = round(rec.score * 100)
            score_label = QLabel(f"Compatibilité estimée : {percentage}%")
            score_label.setStyleSheet("font-size: 15px; font-weight: bold; color: #059669;")

            # Justification (si disponible)
            justification_text = rec.justification if rec.justification else "Correspondance algorithmique forte basée sur vos compétences et votre parcours."
            
            reasons_title = QLabel("Pourquoi ce parcours ?")
            reasons_title.setStyleSheet("font-weight: bold; font-size: 13px; color: #374151;")

            reasons_label = QLabel(f"✓ {justification_text}")
            reasons_label.setWordWrap(True)
            reasons_label.setStyleSheet("color: #4b5563; font-size: 13px;")

            # Assemblage de la carte
            card_layout.addWidget(name)
            card_layout.addWidget(score_label)
            card_layout.addWidget(reasons_title)
            card_layout.addWidget(reasons_label)

            self.results_layout.addWidget(card)

        self.results_layout.addStretch()