from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QLineEdit, QPushButton, QComboBox, QGroupBox,
                             QFormLayout, QRadioButton, QButtonGroup, QScrollArea)
from PyQt5.QtGui import QDoubleValidator
from PyQt5.QtCore import Qt
from PyQt5.QtWebEngineWidgets import QWebEngineView
from geodesic_visualization import GeodesicVisualization
from spherical_calculator import SphericalCalculator
from gauss_calculator import GaussCalculator
import math


class InverseProblemApp(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.spherical_calculator = SphericalCalculator()
        self.gauss_calculator = GaussCalculator()
        self.initUI()

    def initUI(self):
        # Layout horizontal principal
        main_layout = QHBoxLayout()
        main_layout.setSpacing(10)
        main_layout.setContentsMargins(10, 10, 10, 10)

        # Créer un QScrollArea pour la partie gauche
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)

        # Widget conteneur pour la partie gauche
        left_widget = QWidget()
        left_layout = QVBoxLayout()

        # Titre
        title = QLabel("Résolution du Problème Inverse")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("""
            font-size: 28px;
            font-weight: bold;
            color: white;
            background-color: rgba(0, 0, 0, 0.5);
            padding: 10px;
            border-radius: 10px;
            margin: 20px 0;
        """)
        left_layout.addWidget(title)

        # Groupe pour le choix de la méthode
        method_group = QGroupBox("Méthode de calcul")
        method_layout = QHBoxLayout()

        self.method_group = QButtonGroup()
        self.sphere_radio = QRadioButton("Sphère moyenne")
        self.gauss_radio = QRadioButton("Méthode de Gauss")
        self.gauss_radio.setChecked(True)

        self.method_group.addButton(self.sphere_radio)
        self.method_group.addButton(self.gauss_radio)

        method_layout.addWidget(self.sphere_radio)
        method_layout.addWidget(self.gauss_radio)
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

        # Données du premier point
        p1_group = QGroupBox("Point Initial (P1)")
        p1_layout = QFormLayout()
        validator = QDoubleValidator()

        self.phi1_edit = QLineEdit()
        self.phi1_edit.setValidator(validator)
        self.phi1_edit.setPlaceholderText("Ex: 33.5123")
        p1_layout.addRow("Latitude φ1 (°):", self.phi1_edit)

        self.lambda1_edit = QLineEdit()
        self.lambda1_edit.setValidator(validator)
        self.lambda1_edit.setPlaceholderText("Ex: -7.6241")
        p1_layout.addRow("Longitude λ1 (°):", self.lambda1_edit)

        p1_group.setLayout(p1_layout)
        left_layout.addWidget(p1_group)

        # Données du deuxième point
        p2_group = QGroupBox("Point Final (P2)")
        p2_layout = QFormLayout()

        self.phi2_edit = QLineEdit()
        self.phi2_edit.setValidator(validator)
        self.phi2_edit.setPlaceholderText("Ex: 33.6123")
        p2_layout.addRow("Latitude φ2 (°):", self.phi2_edit)

        self.lambda2_edit = QLineEdit()
        self.lambda2_edit.setValidator(validator)
        self.lambda2_edit.setPlaceholderText("Ex: -7.7241")
        p2_layout.addRow("Longitude λ2 (°):", self.lambda2_edit)

        p2_group.setLayout(p2_layout)
        left_layout.addWidget(p2_group)

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
            margin: 10px;
        """)
        left_layout.addWidget(calc_button)

        # Groupe pour les résultats
        results_group = QGroupBox("Résultats")
        results_group.setStyleSheet("background-color: rgba(52, 152, 219, 0.7);")
        results_layout = QVBoxLayout()
        self.distance_result = QLabel("Distance S: ")
        self.alpha12_result = QLabel("Azimut direct α12: ")
        self.alpha21_result = QLabel("Azimut retour α21: ")

        for label in [self.distance_result, self.alpha12_result, self.alpha21_result]:
            label.setStyleSheet("""
                color: white;
                font-size: 16px;
                padding: 5px;
            """)
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
        left_widget.setStyleSheet("background: transparent;")

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
            # Conversion des entrées en radians
            phi1 = math.radians(float(self.phi1_edit.text().replace(',', '.')))
            lambda1 = math.radians(float(self.lambda1_edit.text().replace(',', '.')))
            phi2 = math.radians(float(self.phi2_edit.text().replace(',', '.')))
            lambda2 = math.radians(float(self.lambda2_edit.text().replace(',', '.')))

            # Sélection de l'ellipsoïde
            ellipsoid = self.ellipsoid_combo.currentText()

            # Calcul selon la méthode choisie
            if self.sphere_radio.isChecked():
                calculator = SphericalCalculator(ellipsoid)
                s, alpha12, alpha21 = calculator.inverse_problem(
                    phi1, lambda1, phi2, lambda2
                )
            else:
                calculator = GaussCalculator(ellipsoid)
                s, alpha12, alpha21 = calculator.inverse_problem(
                    phi1, lambda1, phi2, lambda2
                )

            # Conversion des angles en degrés pour l'affichage
            alpha12_deg = math.degrees(alpha12)
            alpha21_deg = math.degrees(alpha21)

            # Affichage des résultats
            self.distance_result.setText(f"Distance S: {s:.3f} m")
            self.alpha12_result.setText(f"Azimut direct α12: {alpha12_deg:.6f}°")
            self.alpha21_result.setText(f"Azimut retour α21: {alpha21_deg:.6f}°")

            # Mise à jour de la visualisation
            self.visualization.update_points(
                float(self.phi1_edit.text().replace(',', '.')),
                float(self.lambda1_edit.text().replace(',', '.')),
                float(self.phi2_edit.text().replace(',', '.')),
                float(self.lambda2_edit.text().replace(',', '.'))
            )

        except ValueError as e:
            error_msg = f"Erreur: {str(e)}" if str(e) else "Erreur: Vérifiez vos entrées"
            self.distance_result.setText(error_msg)
            self.alpha12_result.setText(error_msg)
            self.alpha21_result.setText(error_msg)
        except Exception as e:
            error_msg = f"Erreur inattendue: {str(e)}"
            self.distance_result.setText(error_msg)
            self.alpha12_result.setText(error_msg)
            self.alpha21_result.setText(error_msg)