import numpy as np
import scipy.interpolate


def invert(f, x, kind='linear', vectorized=False):
    """
    Invert a function numerically
    Args:
        f: Function to invert
        x: Domain to invert the function on
        kind: Specifies the kind of interpolation as a string ('linear', 'spline', 'nearest', 'zero', 'slinear',
            'quadratic', 'cubic', 'previous', 'next')
        vectorized: Specifies if the input function is vectorized

    Returns:
    Inverted function with attributes x_min and x_max representing the domain bounds on which the function is defined
    """
    x = np.array(x)
    if not np.issubdtype(x.dtype, np.number):
        raise ValueError('Input domain is not numeric')

    if vectorized:
        y = f(x)
    else:
        y = np.array((f(x_i) for x_i in x))

    if not np.issubdtype(y.dtype, np.number):
        raise ValueError('Input function is not numeric')

    n = len(x)
    y_list = list(y)
    if len(set(y_list)) != n:
        raise ValueError('Non-invertible function')
    
    sorted_y = sorted(y_list)
    if sorted_y != y_list and list(reversed(sorted_y)) != y_list:
        raise ValueError('Non-invertible function')

    if kind == 'spline':
        tck = scipy.interpolate.splrep(y, x)

        def f_inverse(x_new):
            return scipy.interpolate.splev(x_new, tck)

    else:
        f_inverse = scipy.interpolate.interp1d(y, x, kind=kind)

    f_inverse.x_min = min(y)
    f_inverse.x_max = max(y)
    return f_inverse
