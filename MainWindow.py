from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QPushButton, QStackedWidget, QLabel
from PyQt5.QtGui import QFont, QIcon, QPixmap, QPalette, QBrush
from PyQt5.QtCore import Qt, QSize
from coordinate_converter_app import CoordinateConverterApp
from angle_converter_app import AngleConverterApp
from degree_converter_app import DegreeConverterApp
from direct_problem_app import DirectProblemApp
from inverse_problem_app import InverseProblemApp
from PyQt5.QtWidgets import QDesktopWidget

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("GeoTools")
        # Obtenir la taille de l'écran
        screen = QDesktopWidget().availableGeometry()

        # Définir une taille initiale (80% de l'écran)
        initial_width = int(screen.width() * 0.8)
        initial_height = int(screen.height() * 0.8)

        # Définir une taille minimale (60% de l'écran)
        min_width = int(screen.width() * 0.6)
        min_height = int(screen.height() * 0.6)

        # Appliquer la taille minimale
        self.setMinimumSize(min_width, min_height)

        # Définir la taille initiale
        self.resize(initial_width, initial_height)

        # Centrer la fenêtre
        qr = self.frameGeometry()
        cp = screen.center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

        # Définir l'icône de l'application
        self.setWindowIcon(QIcon('./Ressource/icon.png'))


        # Définir l'image de fond avec la propriété NoRepeat
        background = QPixmap('./Ressource/img.png')
        scaled_background = background.scaled(
            self.size(),
            Qt.IgnoreAspectRatio,
            Qt.SmoothTransformation
        )
        palette = QPalette()
        brush = QBrush(scaled_background)
        brush.setStyle(Qt.TexturePattern)  # Utiliser TexturePattern au lieu du pattern par défaut
        palette.setBrush(QPalette.Window, brush)
        self.setPalette(palette)

        # Assurer que le fond suit le redimensionnement de la fenêtre
        self.setAutoFillBackground(True)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.main_layout = QVBoxLayout(central_widget)

        # Titre principal
        # Titre principal
        title_label = QLabel("Géo Tools")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setFont(QFont("Arial", 24, QFont.Bold))
        title_label.setStyleSheet("""
            color: white; 
            background-color: rgba(0, 0, 0, 0.7);
            padding: 20px;
            border-radius: 15px;
            margin: 30px;
            font-size: 36px;
            font-weight: bold;
            border: 2px solid rgba(255, 255, 255, 0.3);
        """)
        self.main_layout.addWidget(title_label)

        self.stacked_widget = QStackedWidget()
        self.main_layout.addWidget(self.stacked_widget)
        self.main_layout.addStretch(1)

        self.menu_page = MenuPage(self)
        self.coordinate_page = self.create_converter_page(CoordinateConverterApp)
        self.angle_page = self.create_converter_page(AngleConverterApp)
        self.degree_page = self.create_converter_page(DegreeConverterApp)

        self.direct_page = self.create_converter_page(DirectProblemApp)
        self.inverse_page = self.create_converter_page(InverseProblemApp)

        self.stacked_widget.addWidget(self.menu_page)
        self.stacked_widget.addWidget(self.coordinate_page)
        self.stacked_widget.addWidget(self.angle_page)
        self.stacked_widget.addWidget(self.degree_page)
        self.stacked_widget.addWidget(self.direct_page)
        self.stacked_widget.addWidget(self.inverse_page)

        creator_label = QLabel("Réalisé par: KHOUSSI Imane")
        creator_label.setAlignment(Qt.AlignRight)
        creator_label.setStyleSheet("""
            color: #FFFFFF; 
            background-color: rgba(0, 0, 0, 0.5);
            padding: 5px;
            border-radius: 5px;
        """)
        self.main_layout.addWidget(creator_label)

    def resizeEvent(self, event):
        """Gérer le redimensionnement de la fenêtre"""
        super().resizeEvent(event)
        # Mettre à jour l'image de fond lors du redimensionnement
        background = QPixmap('./Ressource/img.png')
        scaled_background = background.scaled(
            self.size(),
            Qt.IgnoreAspectRatio,
            Qt.SmoothTransformation
        )
        palette = self.palette()
        brush = QBrush(scaled_background)
        brush.setStyle(Qt.TexturePattern)
        palette.setBrush(QPalette.Window, brush)
        self.setPalette(palette)
    def create_converter_page(self, ConverterClass):
        page = QWidget()
        layout = QVBoxLayout(page)

        converter = ConverterClass(self)
        layout.addWidget(converter)

        back_button = QPushButton("Retour au Menu")
        back_button.setStyleSheet("""
            QPushButton {
                background-color: rgba(52, 152, 219, 0.7);
                color: white;
                border: none;
                padding: 10px;
                border-radius: 5px;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: rgba(41, 128, 185, 0.7);
            }
        """)
        back_button.clicked.connect(self.show_menu)
        layout.addWidget(back_button)

        return page

    def show_menu(self):
        self.stacked_widget.setCurrentWidget(self.menu_page)

    def show_coordinate_converter(self):
        self.stacked_widget.setCurrentWidget(self.coordinate_page)

    def show_angle_converter(self):
        self.stacked_widget.setCurrentWidget(self.angle_page)

    def show_degree_converter(self):
        self.stacked_widget.setCurrentWidget(self.degree_page)


    def show_direct_problem(self):
        """Affiche la page de résolution du problème direct"""
        self.stacked_widget.setCurrentWidget(self.direct_page)

    def show_inverse_problem(self):
        """Affiche la page de résolution du problème inverse"""
        self.stacked_widget.setCurrentWidget(self.inverse_page)

class MenuPage(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        # Ajouter de l'espacement
        layout.setSpacing(20)  # Espacement entre les boutons
        layout.setContentsMargins(50, 50, 50, 50)  # Marges autour des boutons

        buttons = [
            ("Conversion de Coordonnées", self.main_window.show_coordinate_converter),
            ("Conversion d'Angles", self.main_window.show_angle_converter),
            ("Conversion de Degrés", self.main_window.show_degree_converter),
            ("Résolution Problème Direct", self.main_window.show_direct_problem),
            ("Résolution Problème Inverse", self.main_window.show_inverse_problem)
        ]

        for text, callback in buttons:
            btn = QPushButton(text)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: rgba(46, 204, 113, 0.7);
                    color: white;
                    border: 2px solid rgba(255, 255, 255, 0.3);
                    padding: 20px;
                    border-radius: 15px;
                    font-size: 20px;
                    min-width: 400px;
                    margin: 5px;
                    font-weight: bold;
                    text-transform: uppercase;
                }
                QPushButton:hover {
                    background-color: rgba(39, 174, 96, 0.9);
                    border: 2px solid rgba(255, 255, 255, 0.5);
                }
                QPushButton:pressed {
                    background-color: rgba(39, 174, 96, 1.0);
                }
            """)
            btn.clicked.connect(callback)
            layout.addWidget(btn)

        self.setLayout(layout)