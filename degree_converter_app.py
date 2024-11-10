from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QGroupBox, QFormLayout, QTabWidget
from PyQt5.QtGui import QDoubleValidator, QFont
from PyQt5.QtCore import Qt
from conversion_algorithms import DegreeConverter  # Assurez-vous que ce fichier est dans le même dossier

class DegreeConverterApp(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Convertisseur de Degrés")
        self.setGeometry(100, 100, 500, 400)
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
            QLineEdit {
                padding: 6px;
                border: 2px solid #3498db;
                border-radius: 4px;
                background-color: #34495e;
                color: white;
            }
            QLabel {
                color: #ecf0f1;
            }
            QTabWidget::pane {
                border: 1px solid #3498db;
                background-color: #34495e;
            }
            QTabBar::tab {
                background-color: #2c3e50;
                color: white;
                padding: 8px 16px;
                margin-right: 2px;
            }
            QTabBar::tab:selected {
                background-color: #3498db;
            }
        """)

        layout = QVBoxLayout()

        # Titre
        title = QLabel("Convertisseur de Degrés")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            color: #3498db;
            margin: 20px 0;
        """)
        layout.addWidget(title)



        # Création des onglets
        tabs = QTabWidget()
        tabs.addTab(self.create_dd_to_dms_tab(), "DD → DMS")
        tabs.addTab(self.create_dms_to_dd_tab(), "DMS → DD")
        layout.addWidget(tabs)

        self.setLayout(layout)

    def create_dd_to_dms_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()

        input_group = QGroupBox("Degrés Décimaux (DD)")
        input_layout = QFormLayout()

        self.dd_input = QLineEdit()
        self.dd_input.setValidator(QDoubleValidator())
        self.dd_input.setPlaceholderText("Entrez les degrés décimaux")
        input_layout.addRow("DD:", self.dd_input)

        convert_button = QPushButton("Convertir DD → DMS")
        convert_button.clicked.connect(self.convert_dd_to_dms)
        input_layout.addRow(convert_button)

        input_group.setLayout(input_layout)
        layout.addWidget(input_group)

        self.result_dd_to_dms = QLabel("Le résultat s'affichera ici")
        self.result_dd_to_dms.setAlignment(Qt.AlignCenter)
        self.result_dd_to_dms.setStyleSheet("""
            font-size: 18px;
            font-weight: bold;
            color: #2ecc71;
            padding: 10px;
            background-color: #34495e;
            border-radius: 4px;
        """)
        layout.addWidget(self.result_dd_to_dms)

        tab.setLayout(layout)
        return tab

    def create_dms_to_dd_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()

        input_group = QGroupBox("Degrés, Minutes, Secondes (DMS)")
        input_layout = QFormLayout()

        self.d_input = QLineEdit()
        self.d_input.setValidator(QDoubleValidator())
        self.d_input.setPlaceholderText("Degrés")
        input_layout.addRow("Degrés:", self.d_input)

        self.m_input = QLineEdit()
        self.m_input.setValidator(QDoubleValidator())
        self.m_input.setPlaceholderText("Minutes")
        input_layout.addRow("Minutes:", self.m_input)

        self.s_input = QLineEdit()
        self.s_input.setValidator(QDoubleValidator())
        self.s_input.setPlaceholderText("Secondes")
        input_layout.addRow("Secondes:", self.s_input)

        convert_button = QPushButton("Convertir DMS → DD")
        convert_button.clicked.connect(self.convert_dms_to_dd)
        input_layout.addRow(convert_button)

        input_group.setLayout(input_layout)
        layout.addWidget(input_group)

        self.result_dms_to_dd = QLabel("Le résultat s'affichera ici")
        self.result_dms_to_dd.setAlignment(Qt.AlignCenter)
        self.result_dms_to_dd.setStyleSheet("""
            font-size: 18px;
            font-weight: bold;
            color: #2ecc71;
            padding: 10px;
            background-color: #34495e;
            border-radius: 4px;
        """)
        layout.addWidget(self.result_dms_to_dd)

        tab.setLayout(layout)
        return tab

    def convert_dd_to_dms(self):
        try:
            # Remplacer la virgule par un point et convertir en float
            dd = float(self.dd_input.text().replace(',', '.'))

            print(f"Valeur DD extraite: {dd}")  # Logging

            d, m, s = DegreeConverter.dd_to_dms(dd)
            print(f"Résultat de la conversion - D: {d}, M: {m}, S: {s}")  # Logging

            # Formater le résultat en tenant compte des valeurs négatives
            sign = '-' if dd < 0 else ''
            self.result_dd_to_dms.setText(f"{sign}{abs(int(d))}° {int(m)}' {s:.2f}\"")
            self.result_dd_to_dms.setStyleSheet("""
                font-size: 18px;
                font-weight: bold;
                color: #2ecc71;
                padding: 10px;
                background-color: #34495e;
                border-radius: 4px;
            """)
        except ValueError as e:
            print(f"Erreur de conversion: {str(e)}")  # Logging
            self.result_dd_to_dms.setText(f"Erreur: {str(e)}")
            self.result_dd_to_dms.setStyleSheet("""
                font-size: 18px;
                font-weight: bold;
                color: #e74c3c;
                padding: 10px;
                background-color: #34495e;
                border-radius: 4px;
            """)
    def convert_dms_to_dd(self):
        try:
            # Remplacer les virgules par des points et convertir en float
            d = float(self.d_input.text().replace(',', '.'))
            m = float(self.m_input.text().replace(',', '.'))
            s = float(self.s_input.text().replace(',', '.'))

            print(f"Valeurs extraites - D: {d}, M: {m}, S: {s}")  # Logging

            # Vérifier que les valeurs sont dans des plages valides
            if not (0 <= m < 60) or not (0 <= s < 60):
                raise ValueError("Les minutes et secondes doivent être entre 0 et 60")

            dd = DegreeConverter.dms_to_dd(d, m, s)
            print(f"Résultat de la conversion: {dd}")  # Logging

            self.result_dms_to_dd.setText(f"{dd:.6f}°")
            self.result_dms_to_dd.setStyleSheet("""
                font-size: 18px;
                font-weight: bold;
                color: #2ecc71;
                padding: 10px;
                background-color: #34495e;
                border-radius: 4px;
            """)
        except ValueError as e:
            print(f"Erreur de conversion: {str(e)}")  # Logging
            self.result_dms_to_dd.setText(f"Erreur: {str(e)}")
            self.result_dms_to_dd.setStyleSheet("""
                font-size: 18px;
                font-weight: bold;
                color: #e74c3c;
                padding: 10px;
                background-color: #34495e;
                border-radius: 4px;
            """)