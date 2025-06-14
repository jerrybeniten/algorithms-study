import math

class CoordinateDistanceCalculator:

    EARTHS_RADIUS_KM = 6371
    SQUARE = 2
    HALF_ANGLE = 0.5
    DOUBLE = 2
    MAX_HAVERSINE_VALUE = 1

    def __init__(self, 
        longA: float = 0.00, 
        latA: float = 0.00, 
        longB: float = 0.00, 
        latB: float = 0.00
    ):
        self.longA = math.radians(longA)
        self.latA = math.radians(latA)
        self.longB = math.radians(longB)
        self.latB = math.radians(latB)

    # Returns the distiance of point A to point B in kms as the unit.
    # Also known as Haversine Formula.
    def haversine(self) -> float:
             
        latDiff = self.latB - self.latA
        longDiff = self.longB - self.longA

        # Haversine formula
        angularDistanceFactor = (
            math.sin(latDiff * self.HALF_ANGLE) ** self.SQUARE + 
            math.cos(self.latA) * math.cos(self.latB) * 
            math.sin(longDiff * self.HALF_ANGLE) ** self.SQUARE
        )
        
        centralAngle = (
            self.DOUBLE * math.atan2(
                math.sqrt(angularDistanceFactor), 
                math.sqrt(self.MAX_HAVERSINE_VALUE - angularDistanceFactor)
            )
        )

        return self.EARTHS_RADIUS_KM * centralAngle

calculator = CoordinateDistanceCalculator(
    121.1535742,
    14.5232706,
    121.0484840,
    14.5718710
)

print(calculator.haversine())