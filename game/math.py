from typing import Callable


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

        :param t: Smooth step parameter. 0 <= t <= time_constant for smoothed values, outside that range either start
            or stop is returned
        :return: Smoothed value
        """
        if t <= 0:
            return start
        elif t >= time_constant:
            return stop
        else:
            m = t/time_constant
            return (stop-start)*(m*m*3-m*m*m*2)+start
    return smooth_step
