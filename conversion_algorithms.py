import math


class EllipsoidData:
    @staticmethod
    def get_ellipsoid_params(ellipsoid_name):
        ellipsoids = {
            "Clark 1880": {"a": 6378249.145, "f": 1 / 293.4663},
            "WGS84": {"a": 6378137.0, "f": 1 / 298.257223563},
            "GRS80": {"a": 6378137.0, "f": 1 / 298.257222101}
        }
        params = ellipsoids.get(ellipsoid_name)
        if params:
            params["e_squared"] = 2 * params["f"] - params["f"] ** 2
        return params
class CoordinateConverter:
    @staticmethod
    def dms_to_dd(degrees, minutes, seconds):
        return degrees + minutes / 60 + seconds / 3600

    @staticmethod
    def dd_to_dms(decimal_degrees):
        degrees = int(abs(decimal_degrees))
        minutes = int((abs(decimal_degrees) - degrees) * 60)
        seconds = (abs(decimal_degrees) - degrees - minutes / 60) * 3600
        return degrees, minutes, seconds

    @staticmethod
    def geo_to_rect(lat, lon, h, ellipsoid_name):
        params = EllipsoidData.get_ellipsoid_params(ellipsoid_name)
        if not params:
            raise ValueError(f"Ellipsoïde non reconnu : {ellipsoid_name}")

        a, e_squared = params["a"], params["e_squared"]

        lat_rad, lon_rad = math.radians(lat), math.radians(lon)
        sin_lat = math.sin(lat_rad)
        cos_lat = math.cos(lat_rad)
        sin_lon = math.sin(lon_rad)
        cos_lon = math.cos(lon_rad)

        N = a / math.sqrt(1 - e_squared * sin_lat ** 2)

        X = (N + h) * cos_lat * cos_lon
        Y = (N + h) * cos_lat * sin_lon
        Z = (N * (1 - e_squared) + h) * sin_lat

        return X, Y, Z

    @staticmethod
    def rect_to_geo(X, Y, Z, ellipsoid_name, precision=1e-10):
        """
        Convertit les coordonnées rectangulaires (X, Y, Z) en coordonnées géographiques
        en suivant strictement la démarche présentée dans le cours.

        :param X, Y, Z: Coordonnées rectangulaires en mètres
        :param ellipsoid_name: Nom de l'ellipsoïde de référence
        :param precision: Précision souhaitée pour le calcul itératif
        :return: Tuple (latitude, longitude, hauteur)
        """
        params = EllipsoidData.get_ellipsoid_params(ellipsoid_name)
        a, e_squared = params["a"], params["e_squared"]

        # Calcul de la longitude
        lon = math.atan2(Y, X)

        p = math.sqrt(X ** 2 + Y ** 2)

        # Étape 0
        Z_0 = Z / (1 - e_squared)
        tg_phi = Z_0 / p
        phi_0 = math.atan(tg_phi)
        N_0 = a / math.sqrt(1 - e_squared * math.sin(phi_0) ** 2)

        # Étape 1
        Z_1 = Z + N_0 * e_squared * math.sin(phi_0)
        tg_phi = Z_1 / p
        phi_1 = math.atan(tg_phi)
        N_1 = a / math.sqrt(1 - e_squared * math.sin(phi_1) ** 2)

        # Étapes itératives
        i = 1
        while True:
            Z_i = Z + N_1 * e_squared * math.sin(phi_1)
            tg_phi = Z_i / p
            phi_i = math.atan(tg_phi)
            N_i = a / math.sqrt(1 - e_squared * math.sin(phi_i) ** 2)

            if abs(phi_i - phi_1) <= precision:
                break

            phi_1 = phi_i
            N_1 = N_i
            i += 1

        # Calcul de la hauteur ellipsoïdale
        h = p / math.cos(phi_i) - N_i

        # Conversion en degrés
        lat = math.degrees(phi_i)
        lon = math.degrees(lon)

        return lat, lon, h

class AngleConverter:
    @staticmethod
    def convert(angle, from_unit, to_unit):
        if from_unit == to_unit:
            return angle

        # Convertir en radians
        if from_unit == "Degrés":
            rad = math.radians(angle)
        elif from_unit == "Grades":
            rad = angle * (math.pi / 200)
        else:  # Radians
            rad = angle

        # Convertir de radians à l'unité cible
        if to_unit == "Degrés":
            return math.degrees(rad)
        elif to_unit == "Grades":
            return rad * (200 / math.pi)
        else:  # Radians
            return rad


class DegreeConverter:
    @staticmethod
    def dd_to_dms(dd):
        d = int(dd)
        m = int((dd - d) * 60)
        s = (dd - d - m / 60) * 3600
        return d, m, s

    @staticmethod
    def dms_to_dd(d, m, s):
        return d + m / 60 + s / 3600