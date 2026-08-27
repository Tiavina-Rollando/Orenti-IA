from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QFrame,
    QLineEdit,
    QComboBox,
    QScrollArea,
    QGridLayout,
    QDialog,
    QTextEdit,
)


# ============================================================
# DONNÉES DES FILIÈRES ISPM
# ============================================================

FILIERES = [

    # ========================================================
    # INFORMATIQUE ET TÉLÉCOMMUNICATION
    # ========================================================

    {
        "code": "IGGLIA",
        "nom": "Informatique de Gestion, Génie Logiciel et Intelligence Artificielle",
        "domaine": "Informatique et Télécommunications",

        "description":
            "Formation orientée vers la maîtrise des techniques "
            "informatiques appliquées à la gestion des entreprises.",

        "axes": [
            "Informatique de gestion",
            "Génie logiciel",
            "Intelligence artificielle",
            "Systèmes informatiques"
        ],

        "competences": [
            "Conception de logiciels",
            "Développement informatique",
            "Informatique appliquée à la gestion",
            "Analyse des systèmes"
        ],

        "debouches": [
            "Développeur logiciel",
            "Ingénieur logiciel",
            "Analyste informatique",
            "Informaticien de gestion",
            "Métiers liés à l'intelligence artificielle"
        ],

        "prerequis":
            "Baccalauréat C, D, S ou Techniques industrielles.",

        "concours": [
            "Français",
            "Logique ou nombres complexes",
            "Mathématiques"
        ],

        "duree":
            "Licence : 3 ans\nApprofondissement : 2 ans",

    },

    {
        "code": "ESIIA",
        "nom": "Électronique, Système Informatique et Intelligence Artificielle",
        "domaine": "Informatique et Télécommunications",

        "description":
            "Formation combinant l'électronique, la structure "
            "des ordinateurs et les applications fondamentales "
            "de l'informatique.",

        "axes": [
            "Électronique",
            "Systèmes informatiques",
            "Architecture des ordinateurs",
            "Intelligence artificielle"
        ],

        "competences": [
            "Électronique",
            "Compréhension des systèmes informatiques",
            "Architecture des ordinateurs",
            "Informatique appliquée"
        ],

        "debouches": [
            "Ingénieur électronique",
            "Technicien systèmes informatiques",
            "Technicien électronique",
            "Ingénieur informatique",
            "Métiers des systèmes embarqués"
        ],

        "prerequis":
            "Baccalauréat C, D, S ou Techniques industrielles.",

        "concours": [
            "Français",
            "Logique ou nombres complexes",
            "Électricité",
            "Mathématiques"
        ],

        "duree":
            "Licence : 3 ans\nApprofondissement : 2 ans",
    },

    {
        "code": "IMTICIA",
        "nom": "Informatique Multimédia, TIC et Intelligence Artificielle",
        "domaine": "Informatique et Télécommunications",

        "description":
            "Formation consacrée à l'informatique multimédia, "
            "aux télécommunications et aux nouvelles technologies "
            "de l'information et de la communication.",

        "axes": [
            "Informatique multimédia",
            "Technologies de l'information",
            "Communication numérique",
            "Télécommunications",
            "Intelligence artificielle"
        ],

        "competences": [
            "Technologies numériques",
            "Multimédia",
            "Communication numérique",
            "Technologies de l'information"
        ],

        "debouches": [
            "Développeur multimédia",
            "Technicien TIC",
            "Professionnel du numérique",
            "Métiers de la communication numérique",
            "Métiers des télécommunications"
        ],

        "prerequis":
            "Baccalauréat C, D, S ou Techniques industrielles.",

        "concours": [
            "Français",
            "Logique ou nombres complexes",
            "Mathématiques"
        ],

        "duree":
            "Licence : 3 ans\nApprofondissement : 2 ans",
    },

    {
        "code": "ISAIA",
        "nom": "Informatique Statistique Appliquée et Intelligence Artificielle",
        "domaine": "Informatique et Télécommunications",

        "description":
            "Formation basée sur l'application des méthodes "
            "statistiques et informatiques dans différents "
            "domaines de l'économie.",

        "axes": [
            "Mathématiques",
            "Statistiques",
            "Informatique",
            "Économie",
            "Intelligence artificielle"
        ],

        "competences": [
            "Analyse statistique",
            "Traitement des données",
            "Informatique",
            "Analyse économique",
            "Intelligence artificielle"
        ],

        "debouches": [
            "Data analyst",
            "Statisticien",
            "Analyste de données",
            "Analyste économique",
            "Métiers de la banque",
            "Métiers des entreprises industrielles et commerciales"
        ],

        "prerequis":
            "Baccalauréat C, D, S ou Techniques industrielles.",

        "concours": [
            "Français",
            "Logique ou nombres complexes",
            "Mathématiques"
        ],

        "duree":
            "Licence : 3 ans\nApprofondissement : 2 ans",
    },


    # ========================================================
    # TECHNIQUES DES AFFAIRES
    # ========================================================

    {
        "code": "CAA",
        "nom": "Commerce et Administration des Affaires",
        "domaine": "Techniques des Affaires",

        "description":
            "Formation fondée sur le marketing, les techniques "
            "commerciales, l'organisation et le management des entreprises.",

        "axes": [
            "Commerce",
            "Marketing",
            "Techniques commerciales",
            "Organisation",
            "Management"
        ],

        "competences": [
            "Gestion commerciale",
            "Marketing",
            "Management",
            "Organisation d'entreprise",
            "Techniques de vente"
        ],

        "debouches": [
            "Commercial",
            "Responsable commercial",
            "Responsable marketing",
            "Assistant manager",
            "Entrepreneur"
        ],

        "prerequis":
            "Baccalauréat toutes séries.",

        "concours": [
            "Français",
            "Mathématiques ou Histoire-Géographie ou SVT",
            "Anglais ou Allemand ou Espagnol"
        ],

        "duree":
            "Licence : 3 ans\nApprofondissement : 2 ans",
    },

    {
        "code": "FIC",
        "nom": "Finances et Comptabilités",
        "domaine": "Techniques des Affaires",

        "description":
            "Formation consacrée aux techniques quantitatives "
            "de gestion des entreprises, notamment les finances "
            "et la comptabilité.",

        "axes": [
            "Finance",
            "Comptabilité",
            "Gestion",
            "Techniques quantitatives"
        ],

        "competences": [
            "Gestion financière",
            "Comptabilité",
            "Analyse financière",
            "Gestion d'entreprise"
        ],

        "debouches": [
            "Comptable",
            "Assistant comptable",
            "Analyste financier",
            "Gestionnaire",
            "Responsable financier"
        ],

        "prerequis":
            "Baccalauréat toutes séries.",

        "concours": [
            "Français",
            "Mathématiques ou Histoire-Géographie ou SVT",
            "Anglais ou Allemand ou Espagnol"
        ],

        "duree":
            "Licence : 3 ans\nApprofondissement : 2 ans",
    },

    {
        "code": "DTJA",
        "nom": "Droit et Techniques Juridiques des Affaires",
        "domaine": "Techniques des Affaires",

        "description":
            "Formation destinée à maîtriser les techniques "
            "juridiques nationales et internationales avec "
            "l'utilisation de l'outil informatique.",

        "axes": [
            "Droit",
            "Techniques juridiques",
            "Droit des affaires",
            "Outils informatiques"
        ],

        "competences": [
            "Analyse juridique",
            "Techniques juridiques",
            "Droit des affaires",
            "Utilisation des outils informatiques"
        ],

        "debouches": [
            "Juriste",
            "Technicien juridique",
            "Administration publique",
            "Entreprises privées",
            "Services juridiques"
        ],

        "prerequis":
            "Baccalauréat toutes séries.",

        "concours": [
            "Français",
            "Mathématiques ou Histoire-Géographie ou SVT",
            "Anglais ou Allemand ou Espagnol"
        ],

        "duree":
            "Licence : 3 ans\nApprofondissement : 2 ans",
    },

    {
        "code": "EMP",
        "nom": "Économie et Management de Projet",
        "domaine": "Techniques des Affaires",

        "description":
            "Formation visant à former des économistes capables "
            "de réaliser des analyses économiques objectives "
            "et de les appliquer aux réalités des entreprises.",

        "axes": [
            "Économie",
            "Management",
            "Gestion de projet",
            "Analyse économique"
        ],

        "competences": [
            "Analyse économique",
            "Management",
            "Gestion de projet",
            "Prise de décision"
        ],

        "debouches": [
            "Économiste",
            "Chef de projet",
            "Chargé d'études",
            "Consultant",
            "Gestionnaire de projet"
        ],

        "prerequis":
            "Baccalauréat toutes séries.",

        "concours": [
            "Français",
            "Mathématiques ou Histoire-Géographie ou SVT",
            "Anglais ou Allemand ou Espagnol"
        ],

        "duree":
            "Licence : 3 ans\nApprofondissement : 2 ans",
    },


    # ========================================================
    # BIOTECHNOLOGIE ET AGRONOMIE
    # ========================================================

    {
        "code": "IAA",
        "nom": "Industrie Agroalimentaire",
        "domaine": "Biotechnologie et Agronomie",

        "description":
            "Formation destinée à former des cadres pour "
            "les entreprises de l'industrie agroalimentaire.",

        "axes": [
            "Industrie agroalimentaire",
            "Technologies alimentaires",
            "Production",
            "Qualité"
        ],

        "competences": [
            "Production agroalimentaire",
            "Contrôle qualité",
            "Technologies alimentaires",
            "Gestion des procédés"
        ],

        "debouches": [
            "Industrie agroalimentaire",
            "Responsable qualité",
            "Technicien agroalimentaire",
            "Responsable production",
            "Entrepreneur agroalimentaire"
        ],

        "prerequis":
            "Baccalauréat C, D, S, Techniques agricoles "
            "ou A2 avec note ≥ 12 en mathématiques.",

        "concours": [
            "Français",
            "Mathématiques",
            "Chimie ou Biologie"
        ],

        "duree":
            "Licence : 3 ans\nApprofondissement : 2 ans",
    },

    {
        "code": "PIP",
        "nom": "Pharmacologie et Industries Pharmaceutiques",
        "domaine": "Biotechnologie et Agronomie",

        "description":
            "Formation orientée vers l'étude scientifique "
            "des propriétés thérapeutiques, notamment celles "
            "des plantes médicinales.",

        "axes": [
            "Pharmacologie",
            "Industrie pharmaceutique",
            "Biotechnologie",
            "Plantes médicinales"
        ],

        "competences": [
            "Analyse scientifique",
            "Pharmacologie",
            "Biotechnologie",
            "Recherche pharmaceutique"
        ],

        "debouches": [
            "Industrie pharmaceutique",
            "Recherche",
            "Laboratoires",
            "Biotechnologie",
            "Secteur des produits de santé"
        ],

        "prerequis":
            "Baccalauréat C, D, S, Techniques agricoles "
            "ou A2 avec note ≥ 12 en mathématiques.",

        "concours": [
            "Français",
            "Mathématiques",
            "Chimie ou Biologie"
        ],

        "duree":
            "Licence : 3 ans\nApprofondissement : 2 ans",
    },

    {
        "code": "AEE",
        "nom": "Agriculture et Élevage",
        "domaine": "Biotechnologie et Agronomie",

        "description":
            "Formation destinée à appliquer les techniques "
            "et technologies modernes au monde rural et "
            "à développer les concepts d'agri-business.",

        "axes": [
            "Agriculture",
            "Élevage",
            "Technologies agricoles",
            "Agri-business"
        ],

        "competences": [
            "Techniques agricoles",
            "Élevage",
            "Gestion d'exploitation",
            "Agri-business"
        ],

        "debouches": [
            "Exploitant agricole",
            "Conseiller agricole",
            "Gestionnaire d'exploitation",
            "Entrepreneur agricole",
            "Secteur de l'élevage"
        ],

        "prerequis":
            "Baccalauréat C, D, S, Techniques agricoles "
            "ou A2 avec note ≥ 12 en mathématiques.",

        "concours": [
            "Français",
            "Mathématiques",
            "Chimie ou Biologie"
        ],

        "duree":
            "Licence : 3 ans\nApprofondissement : 2 ans",
    },


    # ========================================================
    # GENIE INDUSTRIEL / GENIE CIVIL
    # ========================================================

    {
        "code": "EMII",
        "nom": "Électro-Mécanique et Informatique Industrielle",
        "domaine": "Génie Industriel et Génie Civil",

        "description":
            "Formation combinant les technologies mécaniques, "
            "électriques, industrielles et informatiques.",

        "axes": [
            "Électromécanique",
            "Mécanique",
            "Électricité",
            "Informatique industrielle"
        ],

        "competences": [
            "Maintenance industrielle",
            "Électromécanique",
            "Automatisation",
            "Informatique industrielle"
        ],

        "debouches": [
            "Ingénieur industriel",
            "Technicien de maintenance",
            "Automaticien",
            "Électromécanicien",
            "Industrie manufacturière"
        ],

        "prerequis":
            "Baccalauréat C, D, S ou Techniques industrielles.",

        "concours": [
            "Français",
            "Physique ou RDM",
            "Mathématiques"
        ],

        "duree":
            "Licence : 3 ans\nApprofondissement : 2 ans",
    },

    {
        "code": "GCA",
        "nom": "Génie Civil et Architecture",
        "domaine": "Génie Industriel et Génie Civil",

        "description":
            "Formation orientée vers la construction des "
            "infrastructures, l'aménagement urbain et rural.",

        "axes": [
            "Génie civil",
            "Architecture",
            "Construction",
            "Aménagement urbain",
            "Aménagement rural"
        ],

        "competences": [
            "Conception",
            "Construction",
            "Aménagement",
            "Gestion de projets de construction"
        ],

        "debouches": [
            "Ingénieur génie civil",
            "Architecte",
            "Conducteur de travaux",
            "Bureau d'études",
            "BTP"
        ],

        "prerequis":
            "Baccalauréat C, D, S ou Techniques du génie civil.",

        "concours": [
            "Français",
            "Physique ou RDM",
            "Mathématiques"
        ],

        "duree":
            "Licence : 3 ans\nApprofondissement : 2 ans",
    },

    {
        "code": "ICMP",
        "nom": "Industries Chimiques, Minières et Pétrolières",
        "domaine": "Génie Industriel et Génie Civil",

        "description":
            "Formation destinée aux domaines des industries "
            "chimiques, minières et pétrolières.",

        "axes": [
            "Industrie chimique",
            "Industrie minière",
            "Industrie pétrolière",
            "Technologies industrielles"
        ],

        "competences": [
            "Procédés industriels",
            "Analyse scientifique",
            "Technologies minières",
            "Industrie chimique"
        ],

        "debouches": [
            "Industrie minière",
            "Industrie pétrolière",
            "Industrie chimique",
            "Laboratoires",
            "Bureaux d'études"
        ],

        "prerequis":
            "Baccalauréat C, D, S ou Techniques industrielles.",

        "concours": [
            "Français",
            "Physique ou Chimie",
            "Mathématiques"
        ],

        "duree":
            "Licence : 3 ans\nApprofondissement : 2 ans",
    },


    # ========================================================
    # TOURISME
    # ========================================================

    {
        "code": "TEE",
        "nom": "Tourisme et Environnement",
        "domaine": "Tourisme",

        "description":
            "Formation portant sur la richesse de "
            "l'environnement, de la faune, de la flore "
            "et de la civilisation malagasy.",

        "axes": [
            "Tourisme",
            "Environnement",
            "Patrimoine",
            "Culture",
            "Écotourisme"
        ],

        "competences": [
            "Gestion touristique",
            "Valorisation du patrimoine",
            "Environnement",
            "Communication touristique"
        ],

        "debouches": [
            "Guide touristique",
            "Agence de voyage",
            "Tourisme durable",
            "Gestion de sites touristiques",
            "Organismes touristiques"
        ],

        "prerequis":
            "Baccalauréat toutes séries.",

        "concours": [
            "Français",
            "Mathématiques ou Histoire-Géographie ou SVT",
            "Anglais ou Allemand ou Espagnol"
        ],

        "duree":
            "Licence : 3 ans\nApprofondissement : 2 ans",
    },

    {
        "code": "TEH",
        "nom": "Tourisme et Hôtellerie",
        "domaine": "Tourisme",

        "description":
            "Formation consacrée au tourisme, à la culture "
            "et aux techniques de l'art culinaire national "
            "et international.",

        "axes": [
            "Tourisme",
            "Hôtellerie",
            "Culture",
            "Art culinaire"
        ],

        "competences": [
            "Gestion hôtelière",
            "Accueil",
            "Tourisme",
            "Art culinaire",
            "Communication"
        ],

        "debouches": [
            "Hôtellerie",
            "Restauration",
            "Agences de voyage",
            "Tourisme",
            "Gestion d'établissements touristiques"
        ],

        "prerequis":
            "Baccalauréat toutes séries.",

        "concours": [
            "Français",
            "Mathématiques ou Histoire-Géographie ou SVT",
            "Anglais ou Allemand ou Espagnol"
        ],

        "duree":
            "Licence : 3 ans\nApprofondissement : 2 ans",
    },
]


# ============================================================
# PAGE D'ACCUEIL
# ============================================================

class HomePage(QWidget):

    def __init__(self):
        super().__init__()

        self.setup_ui()
        self.display_filieres()

    # ========================================================
    # INTERFACE
    # ========================================================

    def setup_ui(self):

        layout = QVBoxLayout(self)

        layout.setContentsMargins(
            35, 30, 35, 30
        )

        layout.setSpacing(15)

        # ----------------------------------------------------
        # TITRE
        # ----------------------------------------------------

        title = QLabel(
            "Bienvenue sur ORIENT'IA"
        )

        title.setObjectName(
            "pageTitle"
        )

        subtitle = QLabel(
            "Explorez les formations proposées par "
            "l'Institut Supérieur Polytechnique de Madagascar."
        )

        subtitle.setObjectName(
            "pageSubtitle"
        )

        layout.addWidget(title)
        layout.addWidget(subtitle)

        # ----------------------------------------------------
        # RECHERCHE
        # ----------------------------------------------------

        filters = QHBoxLayout()

        self.search = QLineEdit()

        self.search.setPlaceholderText(
            "🔍 Rechercher une filière..."
        )

        self.search.textChanged.connect(
            self.display_filieres
        )

        self.domain_filter = QComboBox()

        self.domain_filter.addItem(
            "Tous les domaines"
        )

        domains = sorted(
            set(
                f["domaine"]
                for f in FILIERES
            )
        )

        self.domain_filter.addItems(
            domains
        )

        self.domain_filter.currentTextChanged.connect(
            self.display_filieres
        )

        filters.addWidget(
            self.search,
            2
        )

        filters.addWidget(
            self.domain_filter,
            1
        )

        layout.addLayout(filters)

        # ----------------------------------------------------
        # NOMBRE DE FILIÈRES
        # ----------------------------------------------------

        self.count_label = QLabel()

        self.count_label.setStyleSheet(
            "color: #687386; font-size: 13px;"
        )

        layout.addWidget(
            self.count_label
        )

        # ----------------------------------------------------
        # ZONE SCROLLABLE
        # ----------------------------------------------------

        self.scroll = QScrollArea()

        self.scroll.setWidgetResizable(
            True
        )

        self.scroll.setFrameShape(
            QFrame.NoFrame
        )

        self.container = QWidget()

        self.grid = QGridLayout(
            self.container
        )

        self.grid.setSpacing(18)

        self.scroll.setWidget(
            self.container
        )

        layout.addWidget(
            self.scroll
        )

    # ========================================================
    # AFFICHAGE DES FILIÈRES
    # ========================================================

    def display_filieres(self):

        # Supprimer les anciennes cartes

        while self.grid.count():

            item = self.grid.takeAt(0)

            widget = item.widget()

            if widget:

                widget.deleteLater()

        search_text = (
            self.search.text()
            .strip()
            .lower()
        )

        selected_domain = (
            self.domain_filter.currentText()
        )

        filtered = []

        for filiere in FILIERES:

            matches_search = (
                not search_text
                or search_text in filiere["nom"].lower()
                or search_text in filiere["code"].lower()
                or search_text in filiere["domaine"].lower()
            )

            matches_domain = (
                selected_domain == "Tous les domaines"
                or filiere["domaine"] == selected_domain
            )

            if matches_search and matches_domain:

                filtered.append(
                    filiere
                )

        self.count_label.setText(
            f"{len(filtered)} filière(s) trouvée(s)"
        )

        # ----------------------------------------------------
        # CARTES
        # ----------------------------------------------------

        columns = 2

        for index, filiere in enumerate(
            filtered
        ):

            row = index // columns
            column = index % columns

            card = self.create_filiere_card(
                filiere
            )

            self.grid.addWidget(
                card,
                row,
                column
            )

    # ========================================================
    # CARTE FILIÈRE
    # ========================================================

    def create_filiere_card(
        self,
        filiere
    ):

        card = QFrame()

        card.setObjectName(
            "card"
        )

        card.setMinimumHeight(
            260
        )

        layout = QVBoxLayout(
            card
        )

        # ----------------------------------------------------
        # CODE
        # ----------------------------------------------------

        code = QLabel(
            filiere["code"]
        )

        code.setStyleSheet("""
            color: #315efb;
            font-size: 13px;
            font-weight: bold;
        """)

        # ----------------------------------------------------
        # NOM
        # ----------------------------------------------------

        name = QLabel(
            filiere["nom"]
        )

        name.setWordWrap(
            True
        )

        name.setStyleSheet("""
            color: #172033;
            font-size: 18px;
            font-weight: bold;
        """)

        # ----------------------------------------------------
        # DOMAINE
        # ----------------------------------------------------

        domain = QLabel(
            filiere["domaine"]
        )

        domain.setStyleSheet("""
            color: #687386;
            font-size: 13px;
        """)

        # ----------------------------------------------------
        # DUREE
        # ----------------------------------------------------

        duration = QLabel(
            "🎓 " + filiere["duree"].split("\n")[0]
        )

        duration.setStyleSheet("""
            color: #172033;
            font-weight: bold;
        """)

        # ----------------------------------------------------
        # DESCRIPTION
        # ----------------------------------------------------

        description = QLabel(
            filiere["description"]
        )

        description.setWordWrap(
            True
        )

        description.setMaximumHeight(
            55
        )

        description.setStyleSheet("""
            color: #687386;
            font-size: 13px;
        """)

        # ----------------------------------------------------
        # BOUTON
        # ----------------------------------------------------

        button = QPushButton(
            "Voir les détails →"
        )

        button.setObjectName(
            "primaryButton"
        )

        button.clicked.connect(
            lambda checked=False,
            f=filiere:
            self.show_details(f)
        )

        layout.addWidget(
            code
        )

        layout.addWidget(
            name
        )

        layout.addWidget(
            domain
        )

        layout.addWidget(
            duration
        )

        layout.addWidget(
            description
        )

        layout.addStretch()

        layout.addWidget(
            button
        )

        return card

    # ========================================================
    # FENÊTRE DE DÉTAILS
    # ========================================================

    def show_details(
        self,
        filiere
    ):

        dialog = QDialog(
            self
        )

        dialog.setWindowTitle(
            f"{filiere['code']} - {filiere['nom']}"
        )

        dialog.resize(
            750,
            700
        )

        layout = QVBoxLayout(
            dialog
        )

        # ----------------------------------------------------
        # TITRE
        # ----------------------------------------------------

        title = QLabel(
            filiere["nom"]
        )

        title.setWordWrap(
            True
        )

        title.setStyleSheet("""
            color: #172033;
            font-size: 24px;
            font-weight: bold;
        """)

        layout.addWidget(
            title
        )

        code = QLabel(
            f"{filiere['code']} • {filiere['domaine']}"
        )

        code.setStyleSheet("""
            color: #315efb;
            font-size: 14px;
            font-weight: bold;
        """)

        layout.addWidget(
            code
        )

        # ----------------------------------------------------
        # CONTENU
        # ----------------------------------------------------

        content = QTextEdit()

        content.setReadOnly(
            True
        )

        content.setHtml(
            self.build_details_html(
                filiere
            )
        )

        layout.addWidget(
            content
        )

        # ----------------------------------------------------
        # BOUTON FERMER
        # ----------------------------------------------------

        close_button = QPushButton(
            "Fermer"
        )

        close_button.setObjectName(
            "primaryButton"
        )

        close_button.clicked.connect(
            dialog.accept
        )

        layout.addWidget(
            close_button,
            alignment=Qt.AlignRight
        )

        dialog.exec()

    # ========================================================
    # HTML DES DÉTAILS
    # ========================================================

    def build_details_html(
        self,
        f
    ):

        axes = "".join(
            f"<li>{item}</li>"
            for item in f["axes"]
        )

        competences = "".join(
            f"<li>{item}</li>"
            for item in f["competences"]
        )

        debouches = "".join(
            f"<li>{item}</li>"
            for item in f["debouches"]
        )

        concours = "".join(
            f"<li>{item}</li>"
            for item in f["concours"]
        )

        return f"""
        <html>
        <body style="
            font-family: Arial;
            color: #172033;
            font-size: 14px;
        ">

        <h2 style="color:#315efb;">
            Présentation
        </h2>

        <p>
            {f["description"]}
        </p>

        <h2 style="color:#315efb;">
            🎓 Durée de formation
        </h2>

        <p>
            {f["duree"].replace(chr(10), "<br>")}
        </p>

        <h2 style="color:#315efb;">
            📋 Prérequis
        </h2>

        <p>
            {f["prerequis"]}
        </p>

        <h2 style="color:#315efb;">
            📚 Axes principaux de formation
        </h2>

        <ul>
            {axes}
        </ul>

        <h2 style="color:#315efb;">
            🧠 Compétences développées
        </h2>

        <ul>
            {competences}
        </ul>

        <h2 style="color:#315efb;">
            💼 Débouchés possibles
        </h2>

        <ul>
            {debouches}
        </ul>

        <h2 style="color:#315efb;">
            📝 Matières du concours
        </h2>

        <ul>
            {concours}
        </ul>

        </body>
        </html>
        """