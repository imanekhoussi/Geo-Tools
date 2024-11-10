#spherical_calculator.py
import math
from ellipsoid import Ellipsoid
from utils import GeodesicUtils


class SphericalCalculator:
    def __init__(self, ellipsoid_name: str = "Clarke 1880"):

        """
        Initialise le calculateur sphérique avec l'ellipsoïde choisi
        pour obtenir le rayon moyen
        """
        # Choisir l'ellipsoïde de base
        base_ellipsoid = Ellipsoid.CLARKE_1880 if ellipsoid_name == "Clarke 1880" else Ellipsoid.WGS84

        # Obtenir l'ellipsoïde avec les paramètres dérivés
        self.ellipsoid = Ellipsoid.get_derived_params(base_ellipsoid)

        # Obtenir le rayon moyen
        self.R = self.ellipsoid['R_mean']

    def check_distance(self, s: float) -> None:
        if s > 200000:  # 200 km
            raise ValueError("La distance doit être inférieure à 200 km pour le calcul sur sphère")

    def direct_problem(self, phi1: float, lambda1: float, alpha12: float, s: float) -> tuple:
        """
        Résout le problème direct sur la sphère
        Paramètres en radians, distance en mètres
        """
        self.check_distance(s)

        # Distance angulaire
        sigma = s / self.R

        # Calcul de φ2
        sin_phi2 = math.sin(phi1) * math.cos(sigma) + \
                   math.cos(phi1) * math.sin(sigma) * math.cos(alpha12)
        phi2 = math.asin(sin_phi2)

        # Calcul de Δλ
        delta_lambda = math.atan2(
            math.sin(sigma) * math.sin(alpha12),
            math.cos(phi1) * math.cos(sigma) - math.sin(phi1) * math.sin(sigma) * math.cos(alpha12)
        )
        lambda2 = lambda1 + delta_lambda

        # Calcul de α21
        alpha21 = math.atan2(
            math.sin(alpha12),
            math.cos(phi1) * math.tan(phi2) - math.sin(phi1) * math.cos(alpha12)
        ) + math.pi

        return phi2, lambda2, alpha21

    def inverse_problem(self, phi1, lambda1, phi2, lambda2):
        """
        Calcule selon les formules du cours :
        - Distance : cos(σ12) = sin(φ1)sin(φ2) + cos(φ1)cos(φ2)cos(Δλ)
        - Azimut direct : cot(A12) = [tan(φ2)cos(φ1)/sin(Δλ)] - sin(φ1)cot(Δλ)
        - Azimut retour : cot(A21) = -[tan(φ1)cos(φ2)/sin(Δλ)] + sin(φ2)cot(Δλ)
        """
        # Calcul de la distance
        cos_sigma = math.sin(phi1) * math.sin(phi2) + \
                    math.cos(phi1) * math.cos(phi2) * math.cos(lambda2 - lambda1)
        sigma = math.acos(cos_sigma)
        s = sigma * self.R  # Distance métrique

        # Différence de longitude
        delta_lambda = lambda2 - lambda1

        # Azimut direct A12
        cot_A12 = (math.tan(phi2) * math.cos(phi1)) / math.sin(delta_lambda) - \
                  math.sin(phi1) / math.tan(delta_lambda)
        alpha12 = math.atan(1 / cot_A12)

        # Azimut retour A21
        cot_A21 = -(math.tan(phi1) * math.cos(phi2)) / math.sin(delta_lambda) + \
                  math.sin(phi2) / math.tan(delta_lambda)
        alpha21 = math.atan(1 / cot_A21)

        return s, alpha12, alpha21