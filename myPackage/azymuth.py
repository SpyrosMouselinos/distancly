
#!/usr/bin/env python
# -*- coding: utf-8 -*-


import numpy as np
import math


class RhumbLineCalc:
    "A complex calculator for RhumbLine functions"

    def __init__(self):
        self.earth_radius = self.R = 6371
        return

    def is_even(self, n):
        return n % 2 == 0

    def is_odd(self, n):
        return not self.is_even(n)

    def simple_project(self, latitiude):
        return math.tan(math.pi/4 + latitiude/2)

    def mix_project(self, latitiude_b, latitude_a):
        up = self.simple_project(latitiude_b)
        down = self.simple_project(latitude_a)
        total = math.log(up/down)
        return total

    def distance(self,point_a,point_b):
        """
            Returns Rhumbline distance in km between two points
        """
        lat_a = math.radians(point_a[0])
        lon_a = math.radians(point_a[1])

        lat_b = math.radians(point_b[0])
        lon_b = math.radians(point_b[1])

        Δφ = lat_b - lat_a
        Δψ = math.log(self.simple_project(lat_b)/self.simple_project(lat_a))
        Δλ = lon_b - lon_a

        if abs(Δψ) > 10e-12:
            q =  Δφ/Δψ
        else:
            q = math.cos(lat_a)

        if (abs(Δλ) > math.pi):
            if Δλ > 0:
                Δλ = -(2*math.pi-Δλ)
            else:
                Δλ = 2*math.pi+Δλ

        dist = math.sqrt(Δφ*Δφ + q*q*Δλ*Δλ) * self.R
        return dist


    def bearing(self,point_a,point_b):
        """
            Returns bearing between two points in degrees
        """
        lat_a = math.radians(point_a[0])
        lon_a = math.radians(point_a[1])

        lat_b = math.radians(point_b[0])
        lon_b = math.radians(point_b[1])

        Δφ = lat_b - lat_a
        Δψ = math.log(self.simple_project(lat_b)/self.simple_project(lat_a))
        Δλ = lon_b - lon_a

        if (abs(Δλ) > math.pi):
            if Δλ > 0:
                Δλ = -(2*math.pi-Δλ)
            else:
                Δλ = 2*math.pi+Δλ

        brng = math.degrees(math.atan2(Δλ, Δψ))
        return brng


    def destination(self,point_a, bearing, distance, bearing_in='degrees'):
        """
            Returns point B from (point A , constant bearing θ in deg/rad, and distance d in km)
        """
        lat_a = math.radians(point_a[0])
        lon_a = math.radians(point_a[1])
        if bearing_in == 'degrees':
            θ = math.radians(bearing)
        elif bearing_in == 'radians':
            pass
        d = distance
        δ = d/self.R
        Δφ = δ * math.cos(θ)
        lat_b = lat_a + Δφ
        Δψ = math.log(self.simple_project(lat_b)/self.simple_project(lat_a))
        if abs(Δψ) > 10e-12:
            q =  Δφ/Δψ
        else:
            q = math.cos(lat_a)

        Δλ = δ*math.sin(θ)/q
        lon_b = lon_a + Δλ

        # Normalise latitude
        if (abs(lat_b) > math.pi/2):
            if lat_b > 0:
                lat_b = math.pi-lat_b
            else:
                lat_b = -math.pi-lat_b

        lat_b = math.degrees(lat_b)
        lon_b = math.degrees(lon_b)
        # Normalise longitude
        lon_b = (540 + lon_b) % 360 - 180
        return lat_b, lon_b



    def loxodromic_mid_point(self, point_a, point_b):
        """
            Finds the rhumbline mid point between 2 points
        """
        lat_a = math.radians(point_a[0])
        lon_a = math.radians(point_a[1])

        lat_b = math.radians(point_b[0])
        lon_b = math.radians(point_b[1])

        # Anti - Meridian Crossing
        if (abs(lon_b-lon_a) > math.pi):
            lon_a += 2*math.pi

        lat_mid = (lat_a+lat_b)/2
        f1 = self.simple_project(lat_a)
        f2 = self.simple_project(lat_b)
        f3 = self.simple_project(lat_mid)
        if abs(f2 - f1) < 1e-6 :
            lon_mid = lon_a + lon_b / 2
        else:
            lon_mid = ( (lon_b-lon_a)*math.log(f3) + lon_a*math.log(f2) - lon_b*math.log(f1) ) / math.log(f2/f1)


        lat_mid = math.degrees(lat_mid)
        lon_mid = math.degrees(lon_mid)
        # Normalise longitude
        lon_mid = (540 + lon_mid) % 360 - 180
        return lat_mid, lon_mid


    def loxodromic_power_interpolation(self,point_a,point_b,n_points):
        """
            Returns n_points points between point_a and point_b
            according to the rhumbline loxodromic interpolation
        """
        n_points = int(n_points)
        if not math.log2(n_points+1).is_integer():
            print("N_Points must be an power of 2 minus 1 Number! e.g. 1,3,7,15,...")
            return

        lmp = self.loxodromic_mid_point
        # I will try an anadromic_solution

        def solution(a,b,id):
            if id == 1:
                return lmp(a,b)
            else:
                return solution(a,b,1), solution(a,solution(a,b,1),(id-1)/2), solution(solution(a,b,1),b,(id-1)/2)

        points =  solution(point_a,point_b,n_points)
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
    print(rl.loxodromic_mid_point(point_a=(25.7976636,-80.1163316),point_b=(38.7134232,-9.1498182)))
    print(rl.loxodromic_power_interpolation(point_a=(25.7976636,-80.1163316),point_b=(38.7134232,-9.1498182), n_points=7))
