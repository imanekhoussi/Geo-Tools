# GeoTools

Application Python/PyQt5 développée pour le module de Géodésie. Offre des outils de conversion de coordonnées, d'angles, et de degrés, ainsi que la résolution des problèmes géodésiques directs et inverses via une interface graphique intuitive.

## 🚀 Installation

### Prérequis
- Python 3.x
- pip (gestionnaire de paquets Python)

### Dépendances
```bash
pip install PyQt5 PyQtWebEngine
```

### Étapes d'installation
1. Clonez le repository
```bash
git clone https://github.com/votre-username/GeoTools.git
cd GeoTools
```

2. Installez les dépendances
```bash
pip install -r requirements.txt
```

3. Lancez l'application
```bash
python main.py
```

## 📦 Structure du projet
```
GeoTools/
│
├── Ressource/
│   ├── bg.jpg
│   ├── icon.png
│   └── img.png
│
├── main.py
├── MainWindow.py
├── angle_converter_app.py
├── conversion_algorithms.py
├── coordinate_converter_app.py
├── degree_converter_app.py
├── direct_problem_app.py
├── ellipsoid.py
├── gauss_calculator.py
├── geodesic_visualization.py
├── inverse_problem_app.py
├── map.html
├── puissant_calculator.py
├── spherical_calculator.py
└── utils.py
```

## 🔧 Fonctionnalités

- **Conversion de Coordonnées**: Transformation entre différents systèmes de coordonnées
- **Conversion d'Angles**: Conversion entre différents formats d'angles
- **Conversion de Degrés**: Outils de conversion pour les mesures en degrés
- **Problème Direct**: Calcul des coordonnées d'un point à partir d'un point initial et des éléments de distance
- **Problème Inverse**: Calcul des éléments de distance entre deux points connus
- **Visualisation Géodésique**: Affichage des points et lignes géodésiques sur une carte interactive

## 📄 requirements.txt
```
PyQt5==5.15.9
PyQtWebEngine==5.15.9
```

## 👤 Auteure
- KHOUSSI Imane 
- Réalisé dans le cadre du module de Géodésie

## 🗺️ Visualisation
L'application inclut une visualisation interactive des points géodésiques utilisant OpenStreetMap via PyQtWebEngine. Cette fonctionnalité permet de :
- Visualiser les points initiaux et finaux sur une carte
- Afficher la ligne géodésique entre les points
- Zoomer et naviguer interactivement sur la carte

## 📝 License
Ce projet est distribué sous licence [MIT](LICENSE).
