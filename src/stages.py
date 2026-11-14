from equilibrium import x_eq
from operating_lines import rectifying_y, stripping_y, intersection


def step_stages(alpha, R, xD, q, xF, xB, max_stages=500):
    xi, yi = intersection(R, xD, q, xF)
    x = xD
    y = xD
    points = [(x, y)]
    feed_stage = None
    n = 0

    while True:
        n += 1
        if n > max_stages:
            raise ValueError("Too many theoretical stages (R too low, stages never reach xB)")

        x = float(x_eq(y, alpha))             
        points.append((x, y))

        if feed_stage is None and x <= xi:
            feed_stage = n   

        if x <= xB:            
            break

        if x > xi:
            y = float(rectifying_y(x, R, xD))         
        else:
            y = float(stripping_y(x, R, xD, q, xF, xB))        
        points.append((x, y))

    return n, feed_stage, points