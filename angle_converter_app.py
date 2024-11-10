from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QComboBox, QGroupBox, QFormLayout
from PyQt5.QtGui import QDoubleValidator, QFont, QPalette, QColor
from PyQt5.QtCore import Qt
from conversion_algorithms import AngleConverter

class AngleConverterApp(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Convertisseur d'Angles")
        self.setGeometry(100, 100, 400, 300)
        self.setStyleSheet("""
            QWidget {
                background-color: #2c3e50;
                color: #ecf0f1;
                font-family: 'Segoe UI', Arial, sans-serif;
                font-size: 14px;
            }
            QGroupBox {
                border: 2px solid #3498db;
                border-radius: 5px;
                margin-top: 10px;
                font-weight: bold;
                color: #3498db;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 3px 0 3px;
            }
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QLineEdit, QComboBox {
                padding: 6px;
                border: 2px solid #3498db;
                border-radius: 4px;
                background-color: #34495e;
                color: white;
            }
            QLabel {
                color: #ecf0f1;
            }
        """)

        layout = QVBoxLayout()

        # Titre
        title = QLabel("Convertisseur d'Angles")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            color: #3498db;
            margin: 20px 0;
        """)
        layout.addWidget(title)



        # Groupe pour la saisie et la conversion
        input_group = QGroupBox("Conversion d'angles")
        input_layout = QFormLayout()

        self.angle_input = QLineEdit()
        self.angle_input.setValidator(QDoubleValidator())
        self.angle_input.setPlaceholderText("Entrez la valeur de l'angle")
        input_layout.addRow("Angle:", self.angle_input)

        self.input_unit = QComboBox()
        self.input_unit.addItems(["Degrés", "Radians", "Grades"])
        input_layout.addRow("Unité d'entrée:", self.input_unit)

        self.output_unit = QComboBox()
        self.output_unit.addItems(["Degrés", "Radians", "Grades"])
        input_layout.addRow("Convertir en:", self.output_unit)

        convert_button = QPushButton("Convertir")
        convert_button.clicked.connect(self.convert_angle)
        input_layout.addRow(convert_button)

        input_group.setLayout(input_layout)
        layout.addWidget(input_group)

        # Résultat
        result_group = QGroupBox("Résultat")
        result_layout = QVBoxLayout()
        self.result_label = QLabel("Le résultat s'affichera ici")
        self.result_label.setAlignment(Qt.AlignCenter)
        self.result_label.setStyleSheet("""
            font-size: 18px;
            font-weight: bold;
            color: #2ecc71;
            padding: 10px;
            background-color: #34495e;
            border-radius: 4px;
        """)
        result_layout.addWidget(self.result_label)
        result_group.setLayout(result_layout)
        layout.addWidget(result_group)

        self.setLayout(layout)

    def convert_angle(self):
        try:
            angle = float(self.angle_input.text())
            from_unit = self.input_unit.currentText()
            to_unit = self.output_unit.currentText()
            result = AngleConverter.convert(angle, from_unit, to_unit)
            self.result_label.setText(f"{result:.6f} {to_unit}")
            self.result_label.setStyleSheet("""
                font-size: 18px;
                font-weight: bold;
                color: #2ecc71;
                padding: 10px;
                background-color: #34495e;
                border-radius: 4px;
            """)
        except ValueError:
            self.result_label.setText("Erreur: Entrée invalide")
            self.result_label.setStyleSheet("""
                font-size: 18px;
                font-weight: bold;
                color: #e74c3c;
                padding: 10px;
                background-color: #34495e;
                border-radius: 4px;
            """)
