#!/usr/bin/env python
# -*- coding: utf-8 -*-
import math


def simple_project(latitiude: float) -> float:
    """
    Projects a point to its corrected latitude for the rhumbline calculations.
    :param latitiude: A float in radians.
    :return: The projected value in radians.
    """
    return math.tan(math.pi / 4 + latitiude / 2)


def mix_project(latitiude_b: float, latitude_a: float) -> float:
    """
    Projects and returns the log scale of start and end point
    in a rhumbline calculation.
    :param latitiude_b: End Point latitude in radians.
    :param latitude_a: Start Point latitude in radians.
    :return: The log scale of them.
    """
    up = simple_project(latitiude_b)
    down = simple_project(latitude_a)
    total = math.log(up / down)
    return total


def is_even(n: int) -> bool:
    """
    Checks if a number is even(lol).
    :param n: The number.
    :return: True if it is even else false.
    """
    return n % 2 == 0


def is_odd(n: int) -> bool:
    """
    Checks if a number is odd(lol).
    :param n: The number.
    :return: True if it is odd else false.
    """
    return not (n % 2 == 0)


class RhumbLineCalc:
    """A complex calculator for RhumbLine functions"""

    def __init__(self):
        """
            Just store the earth Radius in Here.
        """
        self.earth_radius = self.R = 6371
        return

    def distance(self, point_a: tuple, point_b: tuple) -> float:
        """
        Returns Rhumbline distance in km between two points.
        :param point_a: Start point. Tuple of degrees.
        :param point_b: End point. Tuple of degrees.
        :return: The rhumbline distance in Kilometers.
        """

        lat_a = math.radians(point_a[0])
        lon_a = math.radians(point_a[1])

        lat_b = math.radians(point_b[0])
        lon_b = math.radians(point_b[1])

        delta_phi = lat_b - lat_a
        delta_psi = math.log(simple_project(lat_b) / simple_project(lat_a))
        delta_lambda = lon_b - lon_a

        if abs(delta_psi) > 10e-12:
            q = delta_phi / delta_psi
        else:
            q = math.cos(lat_a)

        if abs(delta_lambda) > math.pi:
            if delta_lambda > 0:
                delta_lambda = -(2 * math.pi - delta_lambda)
            else:
                delta_lambda = 2 * math.pi + delta_lambda

        dist = math.sqrt(delta_phi * delta_phi + q * q * delta_lambda * delta_lambda) * self.R
        return dist

    @staticmethod
    def bearing(point_a: tuple, point_b: tuple) -> float:
        """
        Returns bearing between two points in degrees
        :param point_a: Start point. Tuple of degrees.
        :param point_b: End point. Tuple of degrees.
        :return: The bearing in degrees.
        """
        lat_a = math.radians(point_a[0])
        lon_a = math.radians(point_a[1])

        lat_b = math.radians(point_b[0])
        lon_b = math.radians(point_b[1])

        delta_psi = math.log(simple_project(lat_b) / simple_project(lat_a))
        delta_lambda = lon_b - lon_a

        if abs(delta_lambda) > math.pi:
            if delta_lambda > 0:
                delta_lambda = -(2 * math.pi - delta_lambda)
            else:
                delta_lambda = 2 * math.pi + delta_lambda

        return math.degrees(math.atan2(delta_lambda, delta_psi))

    def destination(self, point_a: tuple, bearing: float, distance: float, bearing_in: str = 'degrees') -> tuple:
        """
        Returns point B from point A, travelling at constant bearing θ in deg/rad, and distance d in km.
        :param point_a: Start point. Tuple of degrees.
        :param bearing: The Bearing in bearing_in.
        :param distance: The Distance in Kilometers.
        :param bearing_in: Whether the bearing is in degrees or radians.
        :return: Point B coordinates.
        """
        lat_a = math.radians(point_a[0])
        lon_a = math.radians(point_a[1])
        theta = bearing
        if bearing_in == 'degrees':
            theta = math.radians(bearing)
        d = distance
        delta = d / self.R
        delta_phi = delta * math.cos(theta)
        lat_b = lat_a + delta_phi
        delta_psi = math.log(simple_project(lat_b) / simple_project(lat_a))
        if abs(delta_psi) > 10e-12:
            q = delta_phi / delta_psi
        else:
            q = math.cos(lat_a)

        delta_lambda = delta * math.sin(theta) / q
        lon_b = lon_a + delta_lambda

        # Normalise latitude
        if abs(lat_b) > math.pi / 2:
            if lat_b > 0:
                lat_b = math.pi - lat_b
            else:
                lat_b = -math.pi - lat_b

        lat_b = math.degrees(lat_b)
        lon_b = math.degrees(lon_b)
        # Normalize longitude
        lon_b = (540 + lon_b) % 360 - 180
        return lat_b, lon_b

    @staticmethod
    def loxodromic_mid_point(point_a: tuple, point_b: tuple) -> tuple:
        """
        Finds the rhumbline mid point between 2 points
        :param point_a: Start point. Tuple of degrees.
        :param point_b: End point. Tuple of degrees.
        :return: The rhumbline midpoint tuple.
        """
        lat_a = math.radians(point_a[0])
        lon_a = math.radians(point_a[1])

        lat_b = math.radians(point_b[0])
        lon_b = math.radians(point_b[1])

        # Anti - Meridian Crossing
        if abs(lon_b - lon_a) > math.pi:
            lon_a += 2 * math.pi

        lat_mid = (lat_a + lat_b) / 2
        f1 = simple_project(lat_a)
        f2 = simple_project(lat_b)
        f3 = simple_project(lat_mid)
        if abs(f2 - f1) < 1e-6:
            lon_mid = lon_a + lon_b / 2
        else:
            lon_mid = ((lon_b - lon_a) * math.log(f3) + lon_a * math.log(f2) - lon_b * math.log(f1)) / math.log(f2 / f1)

        lat_mid = math.degrees(lat_mid)
        lon_mid = math.degrees(lon_mid)
        # Normalize longitude
        lon_mid = (540 + lon_mid) % 360 - 180
        return lat_mid, lon_mid

    def loxodromic_power_interpolation(self, point_a, point_b, n_points):
        """
            Returns n_points points between point_a and point_b
            according to the rhumbline loxodromic interpolation
        """
        n_points = int(n_points)
        if not math.log2(n_points + 1).is_integer():
            print("N_Points must be an power of 2 minus 1 Number! e.g. 1,3,7,15,...")
            return

        lmp = self.loxodromic_mid_point

        # I will try an anadromic_solution

        def solution(a, b, id):
            if id == 1:
                return lmp(a, b)
            else:
                return solution(a, b, 1), solution(a, solution(a, b, 1), (id - 1) / 2), solution(solution(a, b, 1), b,
                                                                                                 (id - 1) / 2)

        points = solution(point_a, point_b, n_points)
        # decouple points #
        decoupled_points = []
        for idx, triplet in enumerate(points):
            if idx == 0:
                singlet = triplet
                decoupled_points.append(singlet)
            else:
                for entry in triplet:
                    decoupled_points.append(entry)
        return decoupled_points


if __name__ == '__main__':
    rl = RhumbLineCalc()
    print(rl.loxodromic_mid_point(point_a=(25.7976636, -80.1163316), point_b=(38.7134232, -9.1498182)))
    print(rl.loxodromic_power_interpolation(point_a=(25.7976636, -80.1163316), point_b=(38.7134232, -9.1498182),
                                            n_points=7))
