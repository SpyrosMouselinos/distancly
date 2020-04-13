## Rhumb Lines Info
*** 
A ‘rhumb line’ (or loxodrome) is a path of constant bearing, which crosses all meridians at the same angle.

Sailors used to (and sometimes still) navigate along rhumb lines since it is easier to follow a constant compass bearing than to be continually adjusting the bearing, as is needed to follow a great circle. Rhumb lines are straight lines on a Mercator Projec­tion map (also helpful for naviga­tion).

Rhumb lines are generally longer than great-circle (orthodrome) routes. For instance, London to New York is 4% longer along a rhumb line than along a great circle – important for avia­tion fuel, but not particularly to sailing vessels. New York to Beijing – close to the most extreme example possible (though not sailable!) – is 30% longer along a rhumb line.

***
### Distance Formula ###
Since a rhumb line is a straight line on a Mercator projec­tion, the distance between two points along a rhumb line is the length of that line (by Pythagoras); but the distor­tion of the projec­tion needs to be compensated for.

On a constant latitude course (travelling east-west), this compensa­tion is simply cosφ; in the general case, it is 

$Δφ/Δψ where Δψ = ln( tan(π/4 + φ2/2) / tan(π/4 + φ1/2) )$ (the ‘projected’ latitude difference)

Formula:	$Δψ = ln( tan(π/4 + φ2/2) / tan(π/4 + φ1/2) )$	(‘projected’ latitude difference)
$q = Δφ/Δψ (or cosφ for E-W line)$
$d = √(Δφ² + q²⋅Δλ²) ⋅ R	(Pythagoras)$
where	φ is latitude, λ is longitude, Δλ is taking shortest route (<180°), R is the earth’s radius, ln is natural log
***
### Bearing Formula ###
A rhumb line is a straight line on a Mercator projection, with an angle on the projec­tion equal to the compass bearing.

Formula:	Δψ = ln( tan(π/4 + φ2/2) / tan(π/4 + φ1/2) )	(‘projected’ latitude difference)
θ = atan2(Δλ, Δψ)	
where	φ is latitude, λ is longitude, Δλ is taking shortest route (<180°), R is the earth’s radius, ln is natural log
***
### Destination Formula ###
Given a start point and a distance d along constant bearing θ, this will calculate the destina­tion point. If you maintain a constant bearing along a rhumb line, you will gradually spiral in towards one of the poles.

Formula:	δ = d/R	(angular distance)
φ2 = φ1 + δ ⋅ cos θ	
Δψ = ln( tan(π/4 + φ2/2) / tan(π/4 + φ1/2) )	(‘projected’ latitude difference)
q = Δφ/Δψ (or cos φ for E-W line)	
Δλ = δ ⋅ sin θ / q	
λ2 = λ1 + Δλ	
where	φ is latitude, λ is longitude, Δλ is taking shortest route (<180°), ln is natural log, R is the earth’s radius
***
### Mid-point Formula ###
This formula for calculating the ‘loxodromic midpoint’, the point half-way along a rhumb line between two points, is due to Robert Hill and Clive Tooth1 (thx Axel!).

Formula:	φm = (φ1+φ2) / 2
f1 = tan(π/4 + φ1/2)
f2 = tan(π/4 + φ2/2)
fm = tan(π/4+φm/2)
λm = [ (λ2−λ1) ⋅ ln(fm) + λ1 ⋅ ln(f2) − λ2 ⋅ ln(f1) ] / ln(f2/f1)
where	φ is latitude, λ is longitude, ln is natural log
