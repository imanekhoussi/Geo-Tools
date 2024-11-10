# gauss_calculator.py
import math
from ellipsoid import Ellipsoid
from utils import GeodesicUtils


class GaussCalculator:
    def __init__(self, ellipsoid_name="Clarke 1880"):
        if ellipsoid_name == "Clarke 1880":
            self.ellipsoid = Ellipsoid.get_derived_params(Ellipsoid.CLARKE_1880)
        else:
            self.ellipsoid = Ellipsoid.get_derived_params(Ellipsoid.WGS84)

    def calculate_N(self, phi):
        """Calcule le rayon de courbure de la première verticale"""
        e_squared = self.ellipsoid['e_squared']
        a = self.ellipsoid['a']
        return a / math.sqrt(1 - e_squared * math.sin(phi) ** 2)

    def calculate_M(self, phi):
        """Calcule le rayon de courbure méridien"""
        e_squared = self.ellipsoid['e_squared']
        a = self.ellipsoid['a']
        return a * (1 - e_squared) / (1 - e_squared * math.sin(phi) ** 2) ** (3 / 2)

    def inverse_problem(self, phi1, lambda1, phi2, lambda2):
        """
        Résolution du problème inverse selon les formules de Gauss Mid-Latitude

        Args:
            phi1, lambda1: Coordonnées du point A (en radians)
            phi2, lambda2: Coordonnées du point B (en radians)

        Returns:
            s: Distance géodésique (en mètres)
            alpha12: Azimut direct (en radians)
            alpha21: Azimut inverse (en radians)
        """
        # 1. Calcul des différences de coordonnées
        delta_lambda = lambda2 - lambda1
        delta_phi = phi2 - phi1

        # 2. Calcul de la latitude moyenne
        phi_m = (phi1 + phi2) / 2

        # 3. Calcul des rayons de courbure au point moyen
        Nm = self.calculate_N(phi_m)
        Mm = self.calculate_M(phi_m)

        # 4. Calcul de delta_alpha/2 selon l'équation (4.29)
        delta_alpha_2 = math.atan2(
            math.tan(delta_lambda / 2) * math.sin(phi_m),
            math.cos(delta_phi / 2)
        )

        # 5. Calcul de (alpha12 + delta_alpha/2) selon l'équation (4.31)
        alpha12_plus_dalpha2 = math.atan2(
            math.cos(phi_m) * math.sin(delta_lambda / 2),
            math.sin(Mm * delta_phi / (2 * Nm))
        )

        # 6. Détermination de alpha12
        alpha12 = alpha12_plus_dalpha2 - delta_alpha_2

        # 7. Calcul de la distance S selon la première équation de (4.29)
        s = Nm * math.cos(phi_m) * delta_lambda / math.sin(alpha12_plus_dalpha2)

        # 8. Vérification avec la deuxième équation de (4.29)
        s_verify = Mm * math.cos(delta_lambda / 2) * delta_phi / math.cos(alpha12_plus_dalpha2)

        # Utiliser la moyenne des deux valeurs de S pour plus de précision
        s = (s + s_verify) / 2

        # 9. Calcul de l'azimut inverse
        alpha21 = alpha12 + math.pi + 2 * delta_alpha_2

        # 10. Normalisation des angles entre 0 et 2π
        alpha12 = GeodesicUtils.normalize_angle(alpha12, 0, 2 * math.pi)
        alpha21 = GeodesicUtils.normalize_angle(alpha21, 0, 2 * math.pi)

        # 11. Validation des résultats
        self._validate_results(s, alpha12, alpha21, phi1, phi2, delta_lambda)

        return s, alpha12, alpha21

    def _validate_results(self, s, alpha12, alpha21, phi1, phi2, delta_lambda):
        """
        Validation des résultats du calcul
        """
        # Vérification de la cohérence des azimuts
        if phi1 > phi2 and delta_lambda > 0:
            assert alpha12 > math.pi, "Azimut direct incorrect pour φ1 > φ2"
        if phi1 < phi2 and delta_lambda < 0:
            assert alpha12 < math.pi, "Azimut direct incorrect pour φ1 < φ2"

        # Vérification de la distance
        max_distance = math.pi * self.ellipsoid['a']  # Distance maximale théorique
        assert 0 < s < max_distance, f"Distance calculée ({s}) hors limites"

    def get_convergence(self, phi, alpha12):
        """
        Calcule la convergence des méridiens
        """
        e_squared = self.ellipsoid['e_squared']
        return math.atan(math.tan(phi) * math.sin(alpha12) /
                         math.sqrt(1 - e_squared * math.sin(phi) ** 2))

    def get_scale_factor(self, phi, alpha12):
        """
        Calcule le facteur d'échelle
        """
        N = self.calculate_N(phi)
        M = self.calculate_M(phi)
        return math.sqrt((N ** 2 * math.cos(alpha12) ** 2 +
                          M ** 2 * math.sin(alpha12) ** 2) / (M * N))