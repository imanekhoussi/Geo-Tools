from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QLineEdit, QPushButton, QComboBox, QGroupBox,
                             QFormLayout, QRadioButton, QButtonGroup, QScrollArea)
from PyQt5.QtGui import QDoubleValidator
from PyQt5.QtCore import Qt
import math
from utils import GeodesicUtils
from spherical_calculator import SphericalCalculator
from puissant_calculator import PuissantCalculator
from geodesic_visualization import GeodesicVisualization


class DirectProblemApp(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.spherical_calculator = SphericalCalculator()
        self.puissant_calculator = PuissantCalculator()
        self.initUI()

    def initUI(self):
        # Layout horizontal principal
        main_layout = QHBoxLayout()
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(20, 20, 20, 20)

        # Créer un QScrollArea pour la partie gauche
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)

        # Widget conteneur pour la partie gauche
        left_widget = QWidget()
        left_layout = QVBoxLayout()
        left_layout.setSpacing(15)

        # Titre
        title = QLabel("Résolution du Problème Direct")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("""
            font-size: 28px;
            font-weight: bold;
            color: white;
            background-color: rgba(0, 0, 0, 0.5);
            padding: 10px;
            border-radius: 10px;
        """)
        left_layout.addWidget(title)

        # Surface de calcul
        method_group = QGroupBox("Surface de calcul")
        method_layout = QHBoxLayout()
        self.method_group = QButtonGroup()
        self.sphere_radio = QRadioButton("Sur la sphère (rayon moyen)")
        self.ellipsoid_radio = QRadioButton("Sur l'ellipsoïde (Puissant)")
        self.sphere_radio.setChecked(True)
        self.method_group.addButton(self.sphere_radio)
        self.method_group.addButton(self.ellipsoid_radio)
        method_layout.addWidget(self.sphere_radio)
        method_layout.addWidget(self.ellipsoid_radio)
        method_group.setLayout(method_layout)
        left_layout.addWidget(method_group)

        # Choix de l'ellipsoïde
        ellipsoid_group = QGroupBox("Ellipsoïde")
        ellipsoid_layout = QFormLayout()
        self.ellipsoid_combo = QComboBox()
        self.ellipsoid_combo.addItems(["Clarke 1880", "WGS84"])
        ellipsoid_layout.addRow("Sélectionner l'ellipsoïde:", self.ellipsoid_combo)
        ellipsoid_group.setLayout(ellipsoid_layout)
        left_layout.addWidget(ellipsoid_group)

        # Données d'entrée
        input_group = QGroupBox("Données d'entrée")
        input_layout = QFormLayout()
        validator = QDoubleValidator()

        self.phi1_edit = QLineEdit()
        self.phi1_edit.setValidator(validator)
        self.phi1_edit.setPlaceholderText("Ex: 33.5123")
        input_layout.addRow("Latitude φ1 (°):", self.phi1_edit)

        self.lambda1_edit = QLineEdit()
        self.lambda1_edit.setValidator(validator)
        self.lambda1_edit.setPlaceholderText("Ex: -7.6241")
        input_layout.addRow("Longitude λ1 (°):", self.lambda1_edit)

        self.alpha12_edit = QLineEdit()
        self.alpha12_edit.setValidator(validator)
        self.alpha12_edit.setPlaceholderText("Ex: 45.0")
        input_layout.addRow("Azimut α12 (°):", self.alpha12_edit)

        self.s_edit = QLineEdit()
        self.s_edit.setValidator(validator)
        self.s_edit.setPlaceholderText("Ex: 10000.0")
        input_layout.addRow("Distance S (m):", self.s_edit)

        input_group.setLayout(input_layout)
        left_layout.addWidget(input_group)

        # Bouton de calcul
        calc_button = QPushButton("Calculer")
        calc_button.clicked.connect(self.calculate)
        calc_button.setStyleSheet("""
            background-color: rgba(46, 204, 113, 0.7);
            color: white;
            border: none;
            padding: 15px;
            border-radius: 8px;
            font-size: 18px;
        """)
        left_layout.addWidget(calc_button)

        # Résultats
        results_group = QGroupBox("Résultats")
        results_group.setStyleSheet("background-color: rgba(52, 152, 219, 0.7);")
        results_layout = QVBoxLayout()
        self.lat2_result = QLabel("Latitude φ2: ")
        self.lon2_result = QLabel("Longitude λ2: ")
        self.alpha21_result = QLabel("Azimut retour α21: ")

        for label in [self.lat2_result, self.lon2_result, self.alpha21_result]:
            label.setStyleSheet("color: white; font-size: 16px; padding: 5px;")
            results_layout.addWidget(label)

        results_group.setLayout(results_layout)
        left_layout.addWidget(results_group)

        # Configuration du widget gauche et du scroll area
        left_widget.setLayout(left_layout)
        scroll.setWidget(left_widget)

        # Style pour le QScrollArea et la barre de défilement
        scroll.setStyleSheet("""
            QScrollArea {
                background: transparent;
                border: none;
            }
            QScrollArea > QWidget > QWidget {
                background: transparent;
            }
            QScrollBar:vertical {
                background: transparent;
                width: 10px;
                margin: 0px;
            }
            QScrollBar::handle:vertical {
                background-color: rgba(52, 152, 219, 0.5);
                min-height: 20px;
                border-radius: 5px;
                margin: 0 2px 0 2px;
            }
            QScrollBar::handle:vertical:hover {
                background-color: rgba(52, 152, 219, 0.7);
            }
            QScrollBar::add-line:vertical {
                height: 0px;
                background: transparent;
            }
            QScrollBar::sub-line:vertical {
                height: 0px;
                background: transparent;
            }
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                background: none;
            }
        """)

        # S'assurer que le widget conteneur est également transparent
        left_widget.setStyleSheet("""
                    background: transparent;
                """)

        # Définir une largeur minimale pour le scroll area
        scroll.setMinimumWidth(400)

        # Ajouter les widgets au layout principal avec des ratios
        main_layout.addWidget(scroll, 2)  # Ratio 2 pour le formulaire avec scrollbar

        # Créer et ajouter la visualisation à droite
        self.visualization = GeodesicVisualization(self)
        main_layout.addWidget(self.visualization, 3)  # Ratio 3 pour la carte

        self.setLayout(main_layout)


        # Styles globaux
        self.setStyleSheet("""
                    QGroupBox {
                        border: 2px solid rgba(52, 152, 219, 0.7);
                        border-radius: 5px;
                        margin-top: 10px;
                        font-weight: bold;
                        color: white;
                        font-size: 14px;
                    }

                    QGroupBox::title {
                        subcontrol-origin: margin;
                        left: 10px;
                        padding: 0 3px 0 3px;
                        font-size: 15px;
                    }

                    QLineEdit {
                        padding: 8px;
                        border: 2px solid rgba(52, 152, 219, 0.7);
                        border-radius: 4px;
                        background-color: rgba(44, 62, 80, 0.7);
                        color: white;
                        font-size: 14px;
                    }

                    QLineEdit:hover {
                        border-color: rgba(52, 152, 219, 0.9);
                        background-color: rgba(44, 62, 80, 0.8);
                    }

                    QLabel {
                        color: white;
                        font-size: 14px;
                        padding: 2px;
                    }

                    QRadioButton {
                        color: white;
                        font-size: 14px;
                        padding: 2px;
                    }

                    QRadioButton::indicator {
                        width: 15px;
                        height: 15px;
                    }

                    QComboBox {
                        padding: 8px;
                        border: 2px solid rgba(52, 152, 219, 0.7);
                        border-radius: 4px;
                        background-color: rgba(44, 62, 80, 0.7);
                        color: white;
                        min-width: 200px;
                        font-size: 14px;
                    }

                    QComboBox:hover {
                        border-color: rgba(52, 152, 219, 0.9);
                        background-color: rgba(44, 62, 80, 0.8);
                    }

                    QComboBox::drop-down {
                        border: none;
                        padding-right: 10px;
                    }

                    QComboBox::down-arrow {
                        width: 12px;
                        height: 12px;
                    }

                    QComboBox QAbstractItemView {
                        border: 2px solid rgba(52, 152, 219, 0.7);
                        border-radius: 4px;
                        background-color: rgba(44, 62, 80, 0.9);
                        color: white;
                        selection-background-color: rgba(52, 152, 219, 0.5);
                        selection-color: white;
                        padding: 4px;
                        font-size: 14px;
                    }

                    QComboBox QAbstractItemView::item {
                        min-height: 30px;
                        padding: 4px;
                    }

                    QComboBox QAbstractItemView::item:hover {
                        background-color: rgba(52, 152, 219, 0.3);
                    }

                    QPushButton {
                        background-color: rgba(46, 204, 113, 0.7);
                        color: white;
                        border: none;
                        padding: 15px;
                        border-radius: 8px;
                        font-size: 18px;
                        margin: 10px;
                    }

                    QPushButton:hover {
                        background-color: rgba(46, 204, 113, 0.9);
                    }

                    QScrollArea {
                        background: transparent;
                        border: none;
                    }

                    QScrollArea > QWidget > QWidget {
                        background: transparent;
                    }

                    QScrollBar:vertical {
                        background: transparent;
                        width: 12px;
                        margin: 0px;
                    }

                    QScrollBar::handle:vertical {
                        background-color: rgba(52, 152, 219, 0.5);
                        min-height: 20px;
                        border-radius: 6px;
                        margin: 0 2px 0 2px;
                    }

                    QScrollBar::handle:vertical:hover {
                        background-color: rgba(52, 152, 219, 0.7);
                    }

                    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                        height: 0px;
                        background: transparent;
                    }

                    QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                        background: none;
                    }
                """)
    def calculate(self):
        try:
            # Récupération des entrées
            phi1 = math.radians(float(self.phi1_edit.text().replace(',', '.')))
            lambda1 = math.radians(float(self.lambda1_edit.text().replace(',', '.')))
            alpha12 = math.radians(float(self.alpha12_edit.text().replace(',', '.')))
            s = float(self.s_edit.text().replace(',', '.'))

            # Choix de l'ellipsoïde
            ellipsoid = "Clarke 1880" if self.ellipsoid_combo.currentText() == "Clarke 1880" else "WGS84"

            # Calcul selon la méthode choisie
            if self.sphere_radio.isChecked():
                calculator = SphericalCalculator(ellipsoid)
            else:
                calculator = PuissantCalculator(ellipsoid)

            # Calcul des résultats
            phi2, lambda2, alpha21 = calculator.direct_problem(phi1, lambda1, alpha12, s)

            # Conversion en degrés pour l'affichage
            phi2_degrees = math.degrees(phi2)
            lambda2_degrees = math.degrees(lambda2)
            alpha21_degrees = math.degrees(alpha21)

            # Affichage des résultats
            self.lat2_result.setText(f"Latitude φ2: {phi2_degrees:.6f}°")
            self.lon2_result.setText(f"Longitude λ2: {lambda2_degrees:.6f}°")
            self.alpha21_result.setText(f"Azimut retour α21: {alpha21_degrees:.6f}°")

            # Mise à jour de la visualisation
            self.visualization.update_points(
                float(self.phi1_edit.text()),
                float(self.lambda1_edit.text()),
                phi2_degrees,
                lambda2_degrees
            )

        except ValueError as e:
            error_msg = "Erreur: Vérifiez vos entrées"
            self.lat2_result.setText(error_msg)
            self.lon2_result.setText(error_msg)
            self.alpha21_result.setText(error_msg)