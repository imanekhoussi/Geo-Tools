from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QRadioButton, QPushButton, QTextEdit, \
    QTabWidget, QComboBox, QGridLayout, QGroupBox, QFormLayout, QApplication, QMainWindow
from PyQt5.QtGui import QDoubleValidator, QFont, QPalette, QColor
from PyQt5.QtCore import Qt, QLocale
from conversion_algorithms import CoordinateConverter


class StyleHelper:
    @staticmethod
    def set_style(app):
        app.setStyle("Fusion")
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(53, 53, 53))
        palette.setColor(QPalette.WindowText, Qt.white)
        palette.setColor(QPalette.Base, QColor(25, 25, 25))
        palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
        palette.setColor(QPalette.ToolTipBase, Qt.white)
        palette.setColor(QPalette.ToolTipText, Qt.white)
        palette.setColor(QPalette.Text, Qt.white)
        palette.setColor(QPalette.Button, QColor(53, 53, 53))
        palette.setColor(QPalette.ButtonText, Qt.white)
        palette.setColor(QPalette.BrightText, Qt.red)
        palette.setColor(QPalette.Link, QColor(42, 130, 218))
        palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
        palette.setColor(QPalette.HighlightedText, Qt.black)
        app.setPalette(palette)


class CoordinateConverterApp(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Convertisseur de Coordonnées")
        self.setGeometry(100, 100, 800, 600)
        self.double_validator = QDoubleValidator()
        self.double_validator.setNotation(QDoubleValidator.StandardNotation)
        locale = QLocale(QLocale.C)
        locale.setNumberOptions(QLocale.RejectGroupSeparator)
        self.double_validator.setLocale(locale)
        self.setStyleSheet("""
            QWidget {
                font-family: 'Segoe UI', Arial, sans-serif;
                font-size: 16px;
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
                background-color: #2c3e50;
                color: white;
            }
            QTextEdit {
                border: 2px solid #3498db;
                border-radius: 4px;
                background-color: #2c3e50;
                color: white;
            }
            QComboBox {
                padding: 6px;
                border: 2px solid #3498db;
                border-radius: 4px;
                background-color: #2c3e50;
                color: white;
            }
            QLabel {
                color: #ecf0f1;
            }
            QRadioButton {
                color: #ecf0f1;
            }
        """)

        main_layout = QVBoxLayout()

        # Titre
        title = QLabel("Convertisseur de Coordonnées Géodésiques")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("""
            font-size: 28px;  /* Augmenté de 24px à 28px */
            font-weight: bold;
            color: white;
            background-color: rgba(52, 152, 219, 0.7);  /* Bleu avec transparence */
            padding: 10px;
            border-radius: 10px;
            margin: 20px 0;
        """)
        main_layout.addWidget(title)



        tabs = QTabWidget()
        tabs.setStyleSheet("""
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
        tabs.addTab(self.create_geo_to_rect_tab(), "Géographique → Cartésien")
        tabs.addTab(self.create_rect_to_geo_tab(), "Cartésien → Géographique")

        main_layout.addWidget(tabs)
        self.setLayout(main_layout)

    def create_geo_to_rect_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()

        # Groupe pour l'ellipsoïde et le format
        input_group = QGroupBox("Paramètres d'entrée")
        input_group_layout = QFormLayout()

        self.ellipsoid_combo = QComboBox()
        self.ellipsoid_combo.addItems(["Clark 1880", "WGS84", "GRS80"])
        input_group_layout.addRow("Ellipsoïde:", self.ellipsoid_combo)

        format_layout = QHBoxLayout()
        self.format_dd = QRadioButton("Degrés décimaux")
        self.format_dms = QRadioButton("DMS")
        self.format_dd.setChecked(True)
        self.format_dd.toggled.connect(self.update_input_fields)
        format_layout.addWidget(self.format_dd)
        format_layout.addWidget(self.format_dms)
        input_group_layout.addRow("Format:", format_layout)

        input_group.setLayout(input_group_layout)
        layout.addWidget(input_group)

        # Groupe pour les champs d'entrée
        self.input_group = QGroupBox("Coordonnées géographiques")
        self.input_grid = QGridLayout()
        self.create_input_fields()
        self.input_group.setLayout(self.input_grid)
        layout.addWidget(self.input_group)

        convert_button = QPushButton("Convertir")
        convert_button.clicked.connect(self.convert_geo_to_rect)
        layout.addWidget(convert_button)

        self.result_geo_to_rect = QTextEdit()
        self.result_geo_to_rect.setReadOnly(True)
        self.result_geo_to_rect.setPlaceholderText("Les résultats de la conversion s'afficheront ici.")
        layout.addWidget(self.result_geo_to_rect)

        tab.setLayout(layout)
        return tab

    def create_rect_to_geo_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()

        input_group = QGroupBox("Coordonnées cartésiennes")
        input_layout = QFormLayout()

        self.ellipsoid_combo_rect = QComboBox()
        self.ellipsoid_combo_rect.addItems(["Clark 1880", "WGS84", "GRS80"])
        input_layout.addRow("Ellipsoïde:", self.ellipsoid_combo_rect)

        double_validator = QDoubleValidator()
        double_validator.setNotation(QDoubleValidator.StandardNotation)

        self.x_entry = QLineEdit()
        self.x_entry.setValidator(double_validator)
        self.x_entry.setPlaceholderText("Ex: 4200000.0")
        input_layout.addRow("X (m):", self.x_entry)

        self.y_entry = QLineEdit()
        self.y_entry.setValidator(double_validator)
        self.y_entry.setPlaceholderText("Ex: 170000.0")
        input_layout.addRow("Y (m):", self.y_entry)

        self.z_entry = QLineEdit()
        self.z_entry.setValidator(double_validator)
        self.z_entry.setPlaceholderText("Ex: 4780000.0")
        input_layout.addRow("Z (m):", self.z_entry)

        input_group.setLayout(input_layout)
        layout.addWidget(input_group)

        output_format_group = QGroupBox("Format de sortie")
        output_format_layout = QHBoxLayout()
        self.output_dd = QRadioButton("Degrés décimaux")
        self.output_dms = QRadioButton("DMS")
        self.output_dd.setChecked(True)
        output_format_layout.addWidget(self.output_dd)
        output_format_layout.addWidget(self.output_dms)
        output_format_group.setLayout(output_format_layout)
        layout.addWidget(output_format_group)

        convert_button = QPushButton("Convertir")
        convert_button.clicked.connect(self.convert_rect_to_geo)
        layout.addWidget(convert_button)

        self.result_rect_to_geo = QTextEdit()
        self.result_rect_to_geo.setReadOnly(True)
        self.result_rect_to_geo.setPlaceholderText("Les résultats de la conversion s'afficheront ici.")
        layout.addWidget(self.result_rect_to_geo)

        tab.setLayout(layout)
        return tab

    def create_input_fields(self):
        for i in reversed(range(self.input_grid.count())):
            self.input_grid.itemAt(i).widget().setParent(None)

        double_validator = QDoubleValidator()
        double_validator.setNotation(QDoubleValidator.StandardNotation)

        if self.format_dd.isChecked():
            self.lat_dd = QLineEdit()
            self.lat_dd.setValidator(double_validator)
            self.lat_dd.setPlaceholderText("Ex: 48.8566")
            self.input_grid.addWidget(QLabel("Latitude (°):"), 0, 0)
            self.input_grid.addWidget(self.lat_dd, 0, 1)

            self.lon_dd = QLineEdit()
            self.lon_dd.setValidator(double_validator)
            self.lon_dd.setPlaceholderText("Ex: 2.3522")
            self.input_grid.addWidget(QLabel("Longitude (°):"), 1, 0)
            self.input_grid.addWidget(self.lon_dd, 1, 1)
        else:
            self.lat_d = QLineEdit()
            self.lat_d.setValidator(double_validator)
            self.lat_d.setPlaceholderText("48")
            self.lat_m = QLineEdit()
            self.lat_m.setValidator(double_validator)
            self.lat_m.setPlaceholderText("51")
            self.lat_s = QLineEdit()
            self.lat_s.setValidator(double_validator)
            self.lat_s.setPlaceholderText("23.81")
            self.input_grid.addWidget(QLabel("Latitude:"), 0, 0)
            self.input_grid.addWidget(self.lat_d, 0, 1)
            self.input_grid.addWidget(QLabel("°"), 0, 2)
            self.input_grid.addWidget(self.lat_m, 0, 3)
            self.input_grid.addWidget(QLabel("'"), 0, 4)
            self.input_grid.addWidget(self.lat_s, 0, 5)
            self.input_grid.addWidget(QLabel("\""), 0, 6)

            self.lon_d = QLineEdit()
            self.lon_d.setValidator(double_validator)
            self.lon_d.setPlaceholderText("2")
            self.lon_m = QLineEdit()
            self.lon_m.setValidator(double_validator)
            self.lon_m.setPlaceholderText("21")
            self.lon_s = QLineEdit()
            self.lon_s.setValidator(double_validator)
            self.lon_s.setPlaceholderText("7.999")
            self.input_grid.addWidget(QLabel("Longitude:"), 1, 0)
            self.input_grid.addWidget(self.lon_d, 1, 1)
            self.input_grid.addWidget(QLabel("°"), 1, 2)
            self.input_grid.addWidget(self.lon_m, 1, 3)
            self.input_grid.addWidget(QLabel("'"), 1, 4)
            self.input_grid.addWidget(self.lon_s, 1, 5)
            self.input_grid.addWidget(QLabel("\""), 1, 6)

        self.h_entry = QLineEdit()
        self.h_entry.setValidator(double_validator)
        self.h_entry.setPlaceholderText("Ex: 100.0")
        self.input_grid.addWidget(QLabel("Hauteur (m):"), 2, 0)
        self.input_grid.addWidget(self.h_entry, 2, 1)

        self.lat_direction = QComboBox()
        self.lat_direction.addItems(["N", "S"])
        self.input_grid.addWidget(self.lat_direction, 0, 7)

        self.lon_direction = QComboBox()
        self.lon_direction.addItems(["E", "O"])
        self.input_grid.addWidget(self.lon_direction, 1, 7)

    def update_input_fields(self):
        self.create_input_fields()

    def convert_geo_to_rect(self):
        try:
            ellipsoid = self.ellipsoid_combo.currentText()
            h = float(self.h_entry.text().replace(',', '.'))

            if self.format_dd.isChecked():
                lat = float(self.lat_dd.text().replace(',', '.'))
                lon = float(self.lon_dd.text().replace(',', '.'))
            else:
                lat = CoordinateConverter.dms_to_dd(
                    float(self.lat_d.text().replace(',', '.')),
                    float(self.lat_m.text().replace(',', '.')),
                    float(self.lat_s.text().replace(',', '.'))
                )
                lon = CoordinateConverter.dms_to_dd(
                    float(self.lon_d.text().replace(',', '.')),
                    float(self.lon_m.text().replace(',', '.')),
                    float(self.lon_s.text().replace(',', '.'))
                )

            if self.lat_direction.currentText() == "S":
                lat = -lat
            if self.lon_direction.currentText() == "O":
                lon = -lon

            X, Y, Z = CoordinateConverter.geo_to_rect(lat, lon, h, ellipsoid)
            result = f"X: {X:.3f} m\nY: {Y:.3f} m\nZ: {Z:.3f} m"
            self.result_geo_to_rect.setPlainText(result)
        except ValueError as e:
            self.result_geo_to_rect.setPlainText(f"Erreur: {str(e)}")

    def convert_rect_to_geo(self):
        try:
            X = float(self.x_entry.text().replace(',', '.'))
            Y = float(self.y_entry.text().replace(',', '.'))
            Z = float(self.z_entry.text().replace(',', '.'))
            ellipsoid = self.ellipsoid_combo_rect.currentText()

            lat, lon, h = CoordinateConverter.rect_to_geo(X, Y, Z, ellipsoid)

            lat_direction = "N" if lat >= 0 else "S"
            lon_direction = "E" if lon >= 0 else "O"
            lat, lon = abs(lat), abs(lon)

            result = ""
            if self.output_dms.isChecked():
                lat_dms = CoordinateConverter.dd_to_dms(lat)
                lon_dms = CoordinateConverter.dd_to_dms(lon)
                result += f"Latitude: {lat_dms[0]}° {lat_dms[1]}' {lat_dms[2]:.2f}\" {lat_direction}\n"
                result += f"Longitude: {lon_dms[0]}° {lon_dms[1]}' {lon_dms[2]:.2f}\" {lon_direction}\n"
            else:
                result += f"Latitude: {lat:.6f}° {lat_direction}\nLongitude: {lon:.6f}° {lon_direction}\n"

            result += f"Hauteur: {h:.3f} m"
            self.result_rect_to_geo.setPlainText(result)
        except ValueError as e:
            self.result_rect_to_geo.setPlainText(f"Erreur: {str(e)}")