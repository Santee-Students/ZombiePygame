import math

'''
def unit_angle(angle):
    """Convert radians to unit circle radians' range of 0 to 6.28"""
    one_rev = math.pi * 2
    if angle > 0:
        return divmod(angle, math.pi * 2)[1]
    if angle < 0:
        angle = divmod(angle, one_rev)[1]
        if angle < 0:
            return angle + one_rev
    return angle
'''

def unit_angle(angle):
    """Convert radians to unit circle radians' range of 0 to 6.28"""
    one_rev = math.pi * 2
    angle = divmod(angle, math.pi * 2)[1]
    if angle < 0:
        return angle + one_rev
    return angle