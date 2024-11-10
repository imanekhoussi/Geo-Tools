import math
from typing import Tuple


class GeodesicUtils:
    @staticmethod
    def normalize_angle(angle: float, min_val: float = -math.pi, max_val: float = math.pi) -> float:
        """Normalise un angle dans l'intervalle [min_val, max_val]"""
        two_pi = 2 * math.pi
        while angle > max_val:
            angle -= two_pi
        while angle < min_val:
            angle += two_pi
        return angle


class Ellipsoid:
    """Définition des ellipsoïdes de référence"""

    CLARKE_1880 = {
        'a': 6378249.145,  # demi grand axe
        'b': 6356514.870,  # demi petit axe
        'e_squared': 0.006803481,  # première excentricité au carré
        'e_prime_squared': 0.006847161  # seconde excentricité au carré
    }

    WGS84 = {
        'a': 6378137.0,  # demi grand axe
        'b': 6356752.314,  # demi petit axe
        'e_squared': 0.006694380,  # première excentricité au carré
        'e_prime_squared': 0.006739497  # seconde excentricité au carré
    }

    @staticmethod
    def get_derived_params(ellipsoid: dict) -> dict:
        """Calcule les paramètres dérivés de l'ellipsoïde"""
        ellipsoid = ellipsoid.copy()
        # Rayon moyen des demi-axes
        ellipsoid['R_mean'] = (2 * ellipsoid['a'] + ellipsoid['b']) / 3
        return ellipsoid


class SphericalCalculator:
    """Calculateur pour la résolution sur la sphère moyenne"""

    def __init__(self, ellipsoid_name: str = "Clarke 1880"):
        """
        Initialise le calculateur avec l'ellipsoïde choisi
        Args:
            ellipsoid_name: Nom de l'ellipsoïde ("Clarke 1880" ou "WGS84")
        """
        if ellipsoid_name == "Clarke 1880":
            self.ellipsoid = Ellipsoid.get_derived_params(Ellipsoid.CLARKE_1880)
        else:
            self.ellipsoid = Ellipsoid.get_derived_params(Ellipsoid.WGS84)

    def check_distance(self, s: float) -> None:
        """
        Vérifie si la distance est valide pour le calcul sur sphère (<200km)
        Args:
            s: Distance en mètres
        Raises:
            ValueError si la distance est trop grande
        """
        if s > 200000:  # 200 km
            raise ValueError("La distance doit être inférieure à 200 km pour le calcul sur sphère")

    def direct_problem(self, phi1: float, lambda1: float, alpha12: float, s: float) -> Tuple[float, float, float]:
        """
        Résout le problème direct sur la sphère moyenne

        Args:
            phi1: Latitude initiale (radians)
            lambda1: Longitude initiale (radians)
            alpha12: Azimut direct (radians)
            s: Distance (mètres)

        Returns:
            Tuple (phi2, lambda2, alpha21) en radians
        """
        self.check_distance(s)
        R = self.ellipsoid['R_mean']

        # Conversion de la distance linéaire en distance angulaire
        sigma = s / R

        # Calcul de la latitude du point d'arrivée
        sin_phi2 = math.sin(phi1) * math.cos(sigma) + \
                   math.cos(phi1) * math.sin(sigma) * math.cos(alpha12)
        phi2 = math.asin(sin_phi2)

        # Calcul de la différence de longitude
        delta_lambda = math.atan2(
            math.sin(sigma) * math.sin(alpha12),
            math.cos(phi1) * math.cos(sigma) - math.sin(phi1) * math.sin(sigma) * math.cos(alpha12)
        )
        lambda2 = GeodesicUtils.normalize_angle(lambda1 + delta_lambda)

        # Calcul de l'azimut retour
        alpha21 = math.atan2(
            math.sin(alpha12),
            math.cos(phi1) * math.tan(phi2) - math.sin(phi1) * math.cos(alpha12)
        ) + math.pi

        alpha21 = GeodesicUtils.normalize_angle(alpha21, 0, 2 * math.pi)

        return phi2, lambda2, alpha21


class PuissantCalculator:
    """Calculateur pour la méthode de Puissant sur l'ellipsoïde"""

    def __init__(self, ellipsoid_name: str = "Clarke 1880"):
        """
        Initialise le calculateur avec l'ellipsoïde choisi
        Args:
            ellipsoid_name: Nom de l'ellipsoïde ("Clarke 1880" ou "WGS84")
        """
        if ellipsoid_name == "Clarke 1880":
            self.ellipsoid = Ellipsoid.get_derived_params(Ellipsoid.CLARKE_1880)
        else:
            self.ellipsoid = Ellipsoid.get_derived_params(Ellipsoid.WGS84)

    def check_distance(self, s: float) -> None:
        """
        Vérifie si la distance est valide pour la méthode de Puissant (<100km)
        Args:
            s: Distance en mètres
        Raises:
            ValueError si la distance est trop grande
        """
        if s > 100000:  # 100 km
            raise ValueError("La distance doit être inférieure à 100 km pour la méthode de Puissant")

    def calculate_N(self, phi: float) -> float:
        """Calcule le rayon de courbure de la première verticale"""
        e_squared = self.ellipsoid['e_squared']
        a = self.ellipsoid['a']
        return a / math.sqrt(1 - e_squared * math.sin(phi) ** 2)

    def calculate_M(self, phi: float) -> float:
        """Calcule le rayon de courbure méridien"""
        e_squared = self.ellipsoid['e_squared']
        a = self.ellipsoid['a']
        return a * (1 - e_squared) / (1 - e_squared * math.sin(phi) ** 2) ** (3 / 2)

    def direct_problem(self, phi1: float, lambda1: float, alpha12: float, s: float) -> Tuple[float, float, float]:
        """
        Résout le problème direct par la méthode de Puissant

        Args:
            phi1: Latitude initiale (radians)
            lambda1: Longitude initiale (radians)
            alpha12: Azimut direct (radians)
            s: Distance (mètres)

        Returns:
            Tuple (phi2, lambda2, alpha21) en radians
        """
        self.check_distance(s)

        # Calcul des éléments au point de départ
        N1 = self.calculate_N(phi1)
        M1 = self.calculate_M(phi1)

        # Coefficients de Puissant
        B = 1 / M1
        C = (3 / 2) * self.ellipsoid['e_squared'] * math.sin(phi1) * math.cos(phi1) / \
            (1 - self.ellipsoid['e_squared'] * math.sin(phi1) ** 2)
        D = math.tan(phi1) / (2 * M1 * N1)
        E = (1 + 3 * math.tan(phi1) ** 2) / (6 * N1 ** 2)
        h = (s / M1) * math.cos(alpha12)

        # Calcul de Δφ
        delta_phi = s * math.cos(alpha12) * B - \
                    s ** 2 * math.sin(alpha12) ** 2 * D - \
                    h * s ** 2 * math.sin(alpha12) ** 2 * E

        # Calcul de φ2
        phi2 = phi1 + delta_phi

        # Calcul de N2
        N2 = self.calculate_N(phi2)

        # Calcul de Δλ
        delta_lambda = s * math.sin(alpha12) / (N2 * math.cos(phi2)) * \
                       (1 - s ** 2 / (6 * N2 ** 2) * (1 - math.sin(alpha12) ** 2 / math.cos(phi2) ** 2))

        # Calcul de λ2
        lambda2 = lambda1 + delta_lambda

        # Calcul de l'azimut retour
        phi_m = (phi1 + phi2) / 2
        delta_alpha = math.atan2(
            math.tan(delta_lambda / 2) * math.sin(phi_m),
            math.cos(delta_phi / 2)
        )

        alpha21 = GeodesicUtils.normalize_angle(alpha12 + math.pi + 2 * delta_alpha, 0, 2 * math.pi)

        return phi2, lambda2, alpha21