# puissant_calculator.py
import math
from ellipsoid import Ellipsoid
from utils import GeodesicUtils


class PuissantCalculator:
    def __init__(self, ellipsoid_name="Clarke 1880"):
        """
        Initialize the Puissant calculator with the chosen ellipsoid
        """
        # Select base ellipsoid
        if ellipsoid_name == "Clarke 1880":
            self.ellipsoid = Ellipsoid.get_derived_params(Ellipsoid.CLARKE_1880)
        else:
            self.ellipsoid = Ellipsoid.get_derived_params(Ellipsoid.WGS84)

        # Store frequently used parameters
        self.e_squared = self.ellipsoid['e_squared']  # Using e_squared instead of e2
        self.a = self.ellipsoid['a']

    def calculate_N(self, phi):
        """Calculate the radius of curvature in the prime vertical"""
        return self.a / math.sqrt(1 - self.e_squared * math.sin(phi) ** 2)

    def calculate_M(self, phi):
        """Calculate the meridian radius of curvature"""
        return self.a * (1 - self.e_squared) / (1 - self.e_squared * math.sin(phi) ** 2) ** (3 / 2)

    def direct_problem(self, phi1, lambda1, alpha12, S):
        """
        Résout le problème direct sur l'ellipsoïde avec les formules de Puissant
        Valable pour des distances jusqu'à 100 km

        Parameters:
        phi1: latitude initiale (radians)
        lambda1: longitude initiale (radians)
        alpha12: azimut initial (radians)
        S: distance (mètres)

        Returns:
        phi2, lambda2, alpha21: coords du point final et azimut retour (radians)
        """
        # 1. Calcul des paramètres fondamentaux au point P1
        M1 = self.calculate_M(phi1)
        N1 = self.calculate_N(phi1)

        # 2. Calcul des coefficients selon les formules du cours
        B = 1 / M1
        C = (3 / 2) * self.e_squared * math.sin(phi1) * math.cos(phi1) / (1 - self.e_squared * math.sin(phi1) ** 2)
        D = math.tan(phi1) / (2 * M1 * N1)
        E = (1 + 3 * math.tan(phi1) ** 2) / (6 * N1 ** 2)

        # 3. Calcul du terme h
        h = (S / M1) * math.cos(alpha12)

        # 4. Calcul de Δφ (différence de latitude)
        # Formule 4.19 du cours
        delta_phi = (S * math.cos(alpha12) * B -
                     S ** 2 * math.sin(alpha12) ** 2 * D -
                     h * S ** 2 * math.sin(alpha12) ** 2 * E)

        # 5. Calcul de la latitude du point final
        phi2 = phi1 + delta_phi

        # 6. Calcul du N2 au point P2
        N2 = self.calculate_N(phi2)

        # 7. Calcul de Δλ (différence de longitude)
        # Formule 4.20 du cours
        delta_lambda = (S / (N2 * math.cos(phi2))) * math.sin(alpha12) * (
                1 - (S ** 2 / (6 * N2 ** 2)) * (1 - math.sin(alpha12) ** 2 * (1 / math.cos(phi2)) ** 2)
        )

        # 8. Calcul de la longitude finale
        lambda2 = lambda1 + delta_lambda

        # 9. Calcul de l'azimut retour selon la formule 4.21
        phi_m = (phi1 + phi2) / 2

        # Calcul de Δα en utilisant la formule de cotangente
        cotg_delta_lambda_2 = math.cos(delta_lambda / 2) / math.sin(delta_lambda / 2)
        cotg_delta_alpha_2 = (math.cos(delta_phi / 2) / math.sin(phi_m)) * cotg_delta_lambda_2
        delta_alpha = 2 * math.atan(1 / cotg_delta_alpha_2)

        # Calcul de l'azimut de retour
        alpha21 = alpha12 - math.pi + delta_alpha  # On utilise - pi (180°)

        # Normalisation de l'azimut entre 0 et 2π
        alpha21 = alpha21 % (2 * math.pi)
        return phi2, lambda2, alpha21
    def inverse_problem(self, phi1, lambda1, phi2, lambda2):
        """
        Solve the inverse geodetic problem using Puissant's formulas

        Parameters:
        phi1, lambda1: coordinates of first point in radians
        phi2, lambda2: coordinates of second point in radians

        Returns:
        tuple: (s, alpha12, alpha21) - distance and azimuths
        """
        # Calculate mean latitude and local radii
        phi_m = (phi1 + phi2) / 2
        M = self.calculate_M(phi_m)
        N = self.calculate_N(phi_m)

        # Calculate coordinate differences
        delta_phi = phi2 - phi1
        delta_lambda = lambda2 - lambda1

        # Calculate distance components
        delta_x = M * delta_phi
        delta_y = N * math.cos(phi_m) * delta_lambda

        # Calculate total distance
        s = math.sqrt(delta_x ** 2 + delta_y ** 2)

        # Calculate forward azimuth
        alpha12 = math.atan2(delta_y, delta_x)

        # Calculate back azimuth
        alpha21 = alpha12 + math.pi

        # Normalize angles
        alpha12 = GeodesicUtils.normalize_angle(alpha12, 0, 2 * math.pi)
        alpha21 = GeodesicUtils.normalize_angle(alpha21, 0, 2 * math.pi)

        return s, alpha12, alpha21