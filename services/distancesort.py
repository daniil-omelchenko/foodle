from math import cos, sqrt

R = 6371000 #radius of the Earth in m


def distance(lon1, lat1, lon2, lat2):
    x = (lon2 - lon1) * cos(0.5*(lat2+lat1))
    y = (lat2 - lat1)
    return R * sqrt( x*x + y*y )

def sort_by_distance(arr, base_lat, base_long):
    return sorted(arr, key= lambda d: distance(d.long, d.lat, base_long, base_lat))
