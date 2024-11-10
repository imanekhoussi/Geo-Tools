#ellipsoid.py
import math


class Ellipsoid:
    """Classe pour gérer les paramètres des ellipsoïdes"""

    CLARKE_1880 = {
        'name': 'Clarke 1880',
        'a': 6378249.145,  # demi grand axe
        'b': 6356514.870,  # demi petit axe
        'f': 1 / 293.4663  # aplatissement
    }

    WGS84 = {
        'name': 'WGS84',
        'a': 6378137.0,
        'b': 6356752.314245,
        'f': 1 / 298.257223563
    }

    @staticmethod
    def get_derived_params(ellipsoid):
        """Calcule les paramètres dérivés de l'ellipsoïde"""
        a = ellipsoid['a']
        b = ellipsoid['b']
        f = ellipsoid['f']

        # Excentricité au carré
        e_squared = 2 * f - f ** 2

        # Rayon moyen
        R_mean = (2 * a + b) / 3

        return {
            **ellipsoid,
            'e_squared': e_squared,
            'R_mean': R_mean
        }
