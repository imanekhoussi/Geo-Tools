# geodesic_visualization.py
from PyQt5.QtWidgets import QWidget, QVBoxLayout
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl
import os


class GeodesicVisualization(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        self.setMinimumWidth(600)  # Largeur minimale augmentée

        # Créer la vue web
        self.web_view = QWebEngineView()
        self.web_view.setMinimumHeight(800)  # Hauteur minimale augmentée

        # HTML pour la carte
        html = """
        <!DOCTYPE html>
        <html>
        <head>
            <link rel="stylesheet" href="https://unpkg.com/leaflet@1.7.1/dist/leaflet.css"/>
            <script src="https://unpkg.com/leaflet@1.7.1/dist/leaflet.js"></script>
            <style>
                body, html {
                    margin: 0;
                    padding: 0;
                    height: 100%;
                    width: 100%;
                }
                #map { 
                    height: 800px;
                    width: 100%;
                    margin: 0;
                    padding: 0;
                }
            </style>
        </head>
        <body>
            <div id="map"></div>
            <script>
                var map = L.map('map').setView([33.5123, -7.6241], 8);
                L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                    attribution: '© OpenStreetMap contributors'
                }).addTo(map);

                var startMarker, endMarker, line;

                window.updateMapFromPython = function(lat1, lon1, lat2, lon2) {
                    if (startMarker) map.removeLayer(startMarker);
                    if (endMarker) map.removeLayer(endMarker);
                    if (line) map.removeLayer(line);

                    startMarker = L.marker([lat1, lon1])
                        .bindPopup('Point initial (φ1, λ1)')
                        .addTo(map);
                    endMarker = L.marker([lat2, lon2])
                        .bindPopup('Point final (φ2, λ2)')
                        .addTo(map);
                    line = L.polyline([[lat1, lon1], [lat2, lon2]], {
                        color: 'red',
                        weight: 3
                    }).addTo(map);

                    map.fitBounds([[lat1, lon1], [lat2, lon2]], {padding: [50, 50]});
                }
            </script>
        </body>
        </html>
        """

        # Sauvegarder le HTML
        html_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "map.html")
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(html)

        # Charger la carte
        self.web_view.setUrl(QUrl.fromLocalFile(html_path))
        layout.addWidget(self.web_view)

        # Supprimer les marges du layout
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.setLayout(layout)

    def update_points(self, lat1, lon1, lat2, lon2):
        js_code = f"updateMapFromPython({lat1}, {lon1}, {lat2}, {lon2})"
        self.web_view.page().runJavaScript(js_code)