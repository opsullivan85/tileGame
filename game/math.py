from typing import Callable
from functools import wraps
from time import time


def constrain(val, min_val, max_val):
    return min(max_val, max(min_val, val))


def get_smooth_step_func(start: float, stop: float, time_constant: float) -> Callable[[float], float]:
    """ Get a function that returns a smooth step between start and stop

    :param start: position to start smoothing at
    :param stop: position to stop smoothing at
    :param time_constant: time constant for smoothing
    :return: A function that returns a smooth step between start and stop
    """

    def smooth_step(t: float) -> float:
        """ Smooth step function

        TODO: Some of this math is implemented wrong. When using Poses the width and height act funny

        :param t: Smooth step parameter. 0 <= t <= time_constant for smoothed values, outside that range either start
            or stop is returned
        :return: Smoothed value
        """
        # print(f'{str(start) = }, {str(stop) = }, {time_constant = }, {t = }')
        if t <= 0:
            return start
        elif t >= time_constant:
            return stop
        else:
            m = t / time_constant
            return (stop - start) * (m * m * 3 - m * m * m * 2) + start

    return smooth_step


def smooth_step(start: float, stop: float, time_constant: float, t: float) -> float:
    """ Smooth step function
    TODO: Some of this math is implemented wrong. When using Poses the width and height act funny
    :param start: position to start smoothing at
    :param stop: position to stop smoothing at
    :param time_constant: time constant for smoothing
    :param t: Smooth step parameter. 0 <= t <= time_constant for smoothed values, outside that range either start
        or stop is returned
    :return: Smoothed value
    """
    if t <= 0:
        return start
    elif t >= time_constant:
        return stop
    else:
        m = t / time_constant
        return (stop - start) * (m * m * 3 - m * m * m * 2) + start


def override_dt_kwarg(func):
    """ Tracks dt and fills in for function calls that don't have it.
    dt is reset every time the function is called, regardless of if dt is included or not.
    Function calls including dt must be kwargs and not args.

    :param func: Function to wrap
    """
    prev_time = time()

    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'dt' in kwargs:
            # dt = kwargs['dt']
            del kwargs['dt']
        # else:
        nonlocal prev_time
        dt = time() - prev_time
        prev_time = time()
        return func(*args, dt=dt, **kwargs)

    return wrapper
