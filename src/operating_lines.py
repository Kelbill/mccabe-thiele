from equilibrium import _check_composition

def rectifying_y(x, R, xD):
    """
    Calculate the y value on the rectifying line for a given x, reflux ratio R, and distillate composition xD.
    
    Parameters:
    x : float or np.ndarray
        The mole fraction of the more volatile component in the liquid phase.
    R : float
        The reflux ratio (must be greater than 0).
    xD : float
        The mole fraction of the more volatile component in the distillate (must be between 0 and 1).
    
    Returns:
    y : float or np.ndarray
        The mole fraction of the more volatile component in the vapor phase on the rectifying line.
    """
    if R <= 0:
        raise ValueError(f"Reflux ratio R must be greater than 0, got {R}")
    _check_composition(xD, "xD")
    
    y = (R / (R + 1)) * x + (1 / (R + 1)) * xD
    return y

def q_line_y(x, q, xF):
    """
    Calculate the y value on the q-line for a given x, feed quality q, and feed composition xF.
    
    Parameters:
    x : float or np.ndarray
        The mole fraction of the more volatile component in the liquid phase.
    q : float
        The feed quality (must be between 0 and 1).
    xF : float
        The mole fraction of the more volatile component in the feed (must be between 0 and 1).
    
    Returns:
    y : float or np.ndarray
        The mole fraction of the more volatile component in the vapor phase on the q-line.
    """
    if not (0 <= q <= 1):
        raise ValueError(f"Feed quality q must be between 0 and 1, got {q}")
    _check_composition(xF, "xF")
    
    y = (q / (q + 1)) * x + (1 / (q + 1)) * xF
    return y

def intersection(R, xD, q, xF):
    """
    Calculate the intersection point of the rectifying line and the q-line.
    
    Parameters:
    R : float
        The reflux ratio (must be greater than 0).
    xD : float
        The mole fraction of the more volatile component in the distillate (must be between 0 and 1).
    q : float
        The feed quality (must be between 0 and 1).
    xF : float
        The mole fraction of the more volatile component in the feed (must be between 0 and 1).
    
    Returns:
    x_intersect : float
        The mole fraction of the more volatile component in the liquid phase at the intersection point.
    y_intersect : float
        The mole fraction of the more volatile component in the vapor phase at the intersection point.
    """
    if R <= 0:
        raise ValueError(f"Reflux ratio R must be greater than 0, got {R}")
    if not (0 <= q <= 1):
        raise ValueError(f"Feed quality q must be between 0 and 1, got {q}")
    _check_composition(xD, "xD")
    _check_composition(xF, "xF")
    
    # Solve for intersection point
    # Rectifying line: y = (R / (R + 1)) * x + (1 / (R + 1)) * xD
    # Q-line: y = (q / (q + 1)) * x + (1 / (q + 1)) * xF
    # Set them equal to find intersection:

    # (R / (R + 1)) * x + (1 / (R + 1)) * xD = (q / (q + 1)) * x + (1 / (q + 1)) * xF
    
    a = R / (R + 1) - q / (q + 1)
    b = (1 / (R + 1)) * xD - (1 / (q + 1)) * xF

    #the eq becomes a*x = b, solve for x, x_intersect = -b / a
    
    if a == 0:
        raise ValueError("The rectifying line and q-line are parallel; no intersection exists.")
    
    x_intersect = b / a
    y_intersect = rectifying_y(x_intersect, R, xD)  # or q_line_y(x_intersect, q, xF), should give same result
    
    return x_intersect, y_intersect
