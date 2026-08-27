import unicodedata

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QFormLayout,
    QLabel,
    QLineEdit,
    QComboBox,
    QTextEdit,
    QPushButton,
    QMessageBox,
    QCheckBox,
    QGroupBox,
    QScrollArea,
    QGridLayout,
    QDoubleSpinBox,
)

from app.data.models import UserProfile
from app.data.loader import load_profile, save_profile


def normalize_key(text: str) -> str:
    """Transforme 'Histoire-Géographie' ou 'Mathématiques' en 'histoire-geographie' / 'mathematiques'."""
    text = text.lower().strip()
    # Supprime les accents
    text = ''.join(
        c for c in unicodedata.normalize('NFD', text)
        if unicodedata.category(c) != 'Mn'
    )
    return text


class ProfilePage(QWidget):

    def __init__(self):
        super().__init__()
        self.setup_ui()
        self.load_existing_profile()

    # =========================================================
    # INTERFACE
    # =========================================================

    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(40, 30, 40, 30)
        main_layout.setSpacing(15)

        # -----------------------------------------------------
        # TITRE & EN-TÊTE
        # -----------------------------------------------------
        title = QLabel("Mon profil")
        title.setObjectName("pageTitle")

        subtitle = QLabel(
            "Renseignez votre profil afin qu'ORIENT'IA puisse analyser vos "
            "préférences et vous proposer les formations les plus adaptées."
        )
        subtitle.setObjectName("pageSubtitle")
        subtitle.setWordWrap(True)

        main_layout.addWidget(title)
        main_layout.addWidget(subtitle)

        # -----------------------------------------------------
        # ZONE SCROLLABLE
        # -----------------------------------------------------
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QScrollArea.NoFrame)

        container = QWidget()
        self.form_layout = QVBoxLayout(container)
        self.form_layout.setSpacing(20)

        # -----------------------------------------------------
        # 1. INFORMATIONS ACADÉMIQUES
        # -----------------------------------------------------
        academic_group = QGroupBox("🎓 Informations académiques")
        academic_layout = QFormLayout(academic_group)
        academic_layout.setSpacing(12)

        self.niveau = QComboBox()
        self.niveau.addItems([
            "",
            "Baccalauréat A",
            "Baccalauréat C",
            "Baccalauréat D",
            "Baccalauréat S",
            "Baccalauréat Technique",
            "Bac+1",
            "Bac+2",
            "Bac+3",
            "Bac+4",
            "Bac+5",
            "Autre",
        ])

        academic_layout.addRow("Niveau d'étude :", self.niveau)
        self.form_layout.addWidget(academic_group)

        # -----------------------------------------------------
        # 2. MATIÈRES PRÉFÉRÉES
        # -----------------------------------------------------
        subjects_group = QGroupBox("📚 Matières préférées")
        subjects_layout = QGridLayout(subjects_group)

        self.subjects = {}
        subjects = [
            "Mathématiques",
            "Physique",
            "Chimie",
            "Informatique",
            "Français",
            "Anglais",
            "Biologie",
            "Économie",
            "Gestion",
            "Histoire-Géographie",
            "Droit",
            "Technique",
        ]

        for index, subject in enumerate(subjects):
            checkbox = QCheckBox(subject)
            self.subjects[subject] = checkbox
            row = index // 3
            column = index % 3
            subjects_layout.addWidget(checkbox, row, column)

        self.form_layout.addWidget(subjects_group)

        # -----------------------------------------------------
        # 3. RÉSULTATS SCOLAIRES
        # -----------------------------------------------------
        grades_group = QGroupBox("📊 Résultats scolaires")
        grades_layout = QGridLayout(grades_group)

        self.grades = {}
        grade_subjects = [
            "Mathématiques",
            "Physique",
            "Chimie",
            "Informatique",
            "Français",
            "Anglais",
            "Biologie",
            "Économie",
            "Gestion",
            "Histoire-Géographie",
            "Droit",
            "Technique",
        ]

        for index, subject in enumerate(grade_subjects):
            label = QLabel(subject)
            spin = QDoubleSpinBox()
            spin.setRange(0, 20)
            spin.setDecimals(2)
            spin.setSingleStep(0.5)
            spin.setValue(0)
            spin.setSuffix(" / 20")

            self.grades[subject] = spin

            row = index // 3
            column = index % 3

            grades_layout.addWidget(label, row * 2, column)
            grades_layout.addWidget(spin, row * 2 + 1, column)

        self.form_layout.addWidget(grades_group)

        # -----------------------------------------------------
        # 4. COMPÉTENCES
        # -----------------------------------------------------
        skills_group = QGroupBox("🧠 Compétences déclarées")
        skills_layout = QVBoxLayout(skills_group)

        self.competences = QLineEdit()
        self.competences.setPlaceholderText(
            "Exemple : Python, SQL, Programmation, Communication, Analyse de données..."
        )
        skills_layout.addWidget(self.competences)

        skills_help = QLabel("Séparez les compétences par des virgules.")
        skills_help.setStyleSheet("color: #687386; font-size: 12px;")
        skills_layout.addWidget(skills_help)

        self.form_layout.addWidget(skills_group)

        # -----------------------------------------------------
        # 5. CENTRES D'INTÉRÊT
        # -----------------------------------------------------
        interests_group = QGroupBox("❤️ Centres d'intérêt")
        interests_layout = QGridLayout(interests_group)

        self.interests = {}
        interests = [
            "Informatique",
            "Intelligence artificielle",
            "Sciences",
            "Technologie",
            "Business",
            "Finance",
            "Agriculture",
            "Santé",
            "Environnement",
            "Droit",
            "Tourisme",
            "Communication",
        ]

        for index, interest in enumerate(interests):
            checkbox = QCheckBox(interest)
            self.interests[interest] = checkbox
            row = index // 3
            column = index % 3
            interests_layout.addWidget(checkbox, row, column)

        self.form_layout.addWidget(interests_group)

        # -----------------------------------------------------
        # 6. ACTIVITÉS / PROJETS
        # -----------------------------------------------------
        projects_group = QGroupBox("🛠️ Activités et projets réalisés")
        projects_layout = QVBoxLayout(projects_group)

        self.projects = QTextEdit()
        self.projects.setPlaceholderText(
            "Décrivez vos projets, activités ou expériences pertinentes.\n\n"
            "Exemple :\n"
            "- Création d'une application Python\n"
            "- Projet Arduino\n"
            "- Participation à un hackathon"
        )
        self.projects.setMaximumHeight(130)
        projects_layout.addWidget(self.projects)

        projects_help = QLabel("Une activité ou un projet par ligne.")
        projects_help.setStyleSheet("color: #687386; font-size: 12px;")
        projects_layout.addWidget(projects_help)

        self.form_layout.addWidget(projects_group)

        # -----------------------------------------------------
        # 7. PRÉFÉRENCES PROFESSIONNELLES
        # -----------------------------------------------------
        jobs_group = QGroupBox("💼 Préférences professionnelles")
        jobs_layout = QGridLayout(jobs_group)

        self.jobs = {}
        jobs = [
            "Développeur logiciel",
            "Data Scientist",
            "Ingénieur",
            "Entrepreneur",
            "Comptable",
            "Manager",
            "Commercial",
            "Chercheur",
            "Technicien",
            "Architecte",
            "Agronome",
            "Professionnel du tourisme",
        ]

        for index, job in enumerate(jobs):
            checkbox = QCheckBox(job)
            self.jobs[job] = checkbox
            row = index // 3
            column = index % 3
            jobs_layout.addWidget(checkbox, row, column)

        self.form_layout.addWidget(jobs_group)

        # -----------------------------------------------------
        # 8. ENVIRONNEMENT DE TRAVAIL
        # -----------------------------------------------------
        environment_group = QGroupBox("🏢 Environnement de travail recherché")
        environment_layout = QGridLayout(environment_group)

        self.environments = {}
        environments = [
            "Travail en équipe",
            "Travail individuel",
            "Bureau",
            "Laboratoire",
            "Terrain",
            "Entreprise",
            "Administration",
            "Environnement industriel",
            "Environnement international",
            "Télétravail",
        ]

        for index, environment in enumerate(environments):
            checkbox = QCheckBox(environment)
            self.environments[environment] = checkbox
            row = index // 3
            column = index % 3
            environment_layout.addWidget(checkbox, row, column)

        self.form_layout.addWidget(environment_group)

        self.form_layout.addStretch()
        scroll.setWidget(container)
        main_layout.addWidget(scroll)

        # -----------------------------------------------------
        # BOUTONS D'ACTION
        # -----------------------------------------------------
        button_layout = QHBoxLayout()
        button_layout.addStretch()

        self.reset_button = QPushButton("↻ Réinitialiser")
        self.reset_button.clicked.connect(self.reset_form)

        self.save_button = QPushButton("💾 Enregistrer le profil")
        self.save_button.setObjectName("primaryButton")
        self.save_button.clicked.connect(self.save)

        button_layout.addWidget(self.reset_button)
        button_layout.addWidget(self.save_button)

        main_layout.addLayout(button_layout)

        # -----------------------------------------------------
        # FEUILLE DE STYLE (QSS)
        # -----------------------------------------------------
        self.setStyleSheet("""
            QLabel {
                color: #1f2937;
            }

            QGroupBox {
                color: #1f2937;
                background-color: #ffffff;
                border: 1px solid #d1d5db;
                border-radius: 8px;
                margin-top: 12px;
                padding: 15px;
                font-size: 15px;
                font-weight: bold;
            }

            QGroupBox::title {
                color: #1f2937;
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
                background-color: #ffffff;
            }

            QCheckBox {
                color: #1f2937;
                background-color: transparent;
                font-size: 13px;
                font-weight: normal;
            }

            QLineEdit, QTextEdit, QComboBox, QDoubleSpinBox {
                color: #1f2937;
                background-color: #ffffff;
                border: 1px solid #d1d5db;
                border-radius: 6px;
                padding: 6px;
            }

            QLineEdit:focus, QTextEdit:focus, QComboBox:focus, QDoubleSpinBox:focus {
                border: 1px solid #2563eb;
            }

            QComboBox QAbstractItemView {
                color: #1f2937;
                background-color: #ffffff;
                selection-background-color: #e5e7eb;
                selection-color: #1f2937;
            }

            QScrollArea {
                background-color: #f5f7fb;
                border: none;
            }

            QScrollArea QWidget {
                background-color: #f5f7fb;
            }

            QPushButton {
                color: #1f2937;
            }

            QLabel#pageTitle {
                color: #111827;
            }

            QLabel#pageSubtitle {
                color: #687386;
            }
            /* Ajouter à la fin de self.setStyleSheet() */

            QMessageBox {
                background-color: #ffffff;
            }

            QMessageBox QLabel {
                color: #1f2937;
                background-color: transparent;
            }

            QMessageBox QPushButton {
                color: #ffffff;
                background-color: #2563eb;
                border-radius: 4px;
                padding: 6px 14px;
                min-width: 60px;
            }

            QMessageBox QPushButton:hover {
                background-color: #1d4ed8;
            }
            
        """)

    # =========================================================
    # CHARGEMENT DU PROFIL
    # =========================================================

    def load_existing_profile(self):
        profile = load_profile()
        if profile is None:
            return

        # Niveau
        index = self.niveau.findText(profile.niveau)
        if index >= 0:
            self.niveau.setCurrentIndex(index)

        # Matières préférées
        for subject in profile.matieres_preferees:
            if subject in self.subjects:
                self.subjects[subject].setChecked(True)

        # Notes scolaires (Recherche par clé normalisée)
        for subject_name, spin in self.grades.items():
            normalized = normalize_key(subject_name)
            if normalized in profile.resultats_scolaires:
                spin.setValue(profile.resultats_scolaires[normalized])

        # Compétences
        self.competences.setText(", ".join(profile.competences))

        # Centres d'intérêt
        for interest in profile.centres_interet:
            if interest in self.interests:
                self.interests[interest].setChecked(True)

        # Projets
        self.projects.setPlainText("\n".join(profile.activites_projets))

        # Préférences professionnelles
        for job in profile.preferences_professionnelles:
            if job in self.jobs:
                self.jobs[job].setChecked(True)

        # Environnement de travail
        for environment in profile.environnement_travail:
            if environment in self.environments:
                self.environments[environment].setChecked(True)

    # =========================================================
    # ENREGISTREMENT
    # =========================================================

    def save(self):
        matieres_preferees = [
            subject for subject, checkbox in self.subjects.items()
            if checkbox.isChecked()
        ]

        # Normalisation des clés pour correspondre au dataset ML
        resultats_scolaires = {
            normalize_key(subject): spin.value()
            for subject, spin in self.grades.items()
            if spin.value() > 0
        }

        competences = [
            item.strip()
            for item in self.competences.text().split(",")
            if item.strip()
        ]

        centres_interet = [
            interest for interest, checkbox in self.interests.items()
            if checkbox.isChecked()
        ]

        activites_projets = [
            line.strip()
            for line in self.projects.toPlainText().splitlines()
            if line.strip()
        ]

        preferences_professionnelles = [
            job for job, checkbox in self.jobs.items()
            if checkbox.isChecked()
        ]

        environnement_travail = [
            environment for environment, checkbox in self.environments.items()
            if checkbox.isChecked()
        ]

        profile = UserProfile(
            niveau=self.niveau.currentText(),
            matieres_preferees=matieres_preferees,
            resultats_scolaires=resultats_scolaires,
            competences=competences,
            centres_interet=centres_interet,
            activites_projets=activites_projets,
            preferences_professionnelles=preferences_professionnelles,
            environnement_travail=environnement_travail,
        )

        try:
            save_profile(profile)
            QMessageBox.information(
                self,
                "Profil enregistré",
                "Votre profil a été enregistré avec succès.\n\n"
                "Ces informations pourront maintenant être utilisées pour générer vos recommandations."
            )
        except Exception as e:
            QMessageBox.critical(
                self,
                "Erreur",
                f"Impossible d'enregistrer le profil.\n\nErreur : {e}"
            )

    # =========================================================
    # RÉINITIALISATION
    # =========================================================

    def reset_form(self):
        self.niveau.setCurrentIndex(0)

        for checkbox in self.subjects.values():
            checkbox.setChecked(False)

        for spin in self.grades.values():
            spin.setValue(0)

        self.competences.clear()

        for checkbox in self.interests.values():
            checkbox.setChecked(False)

        self.projects.clear()

        for checkbox in self.jobs.values():
            checkbox.setChecked(False)

        for checkbox in self.environments.values():
            checkbox.setChecked(False)