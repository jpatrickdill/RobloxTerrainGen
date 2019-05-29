import math


# simple modifier functions

def circle_island(inner=0.2, outer=0.9, center=(0, 0)):
    # returns modifier that creates an integral island by subtracting outer circle

    def modifier(value, coord, config):
        bounds = config["bounds"]

        radius = ((bounds[1][0] - bounds[0][0]) / 2 + (bounds[1][1] - bounds[0][1]) / 2) / 2

        dist = math.sqrt((coord[0] - center[0]) ** 2 + (coord[1] - center[1]) ** 2)
        a = dist / radius

        sub = 0

        if inner <= a <= outer:
            sub = (a - inner) / (outer - inner)
        elif a > outer:
            sub = 1

        value.height = max(0, value.height - sub)

        return value

    return modifier
