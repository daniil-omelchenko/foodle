from math import cos, sqrt, radians


R = 6371000  # radius of the Earth in m


def distance(d, base):
    lon1, lat1, lon2, lat2 = radians(d.lon), radians(d.lat), radians(base.lon), radians(base.lat)
    x = (lon2 - lon1) * cos(0.5 * (lat2 + lat1))
    y = (lat2 - lat1)
    d.distance = R * sqrt(x * x + y * y)
    return d.distance


def sort_by_distance(arr, base):
    return sorted(arr, key=lambda d: distance(d, base))
