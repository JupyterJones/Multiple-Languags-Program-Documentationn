def SimplePSO(func, x0, args=(), niter=50):
    """
    Simple Particle Swarm Optimization (SimplePSO) algorithm.
    The positions of particles are updated by
        x = x + 2 * rand() * (pb - x) + 2 * rand() * (gb - x)

    Parameters
    ----------
    func: callable
        Objective function y = func(x, *args) where 
            x has shape of (n,) or (m, n) and
            y has shape of () or (m,) correspondingly.
    x0: shape(m, n)
        Initial positions of particle swarm, m is the number of particles, 
        n is the dimension of parameters.
    args : tuple, optional
        Extra arguments passed to the objective function.
    niter : int
        Number of iterations to perform.

    Example
    -------
    from scipy.optimize import rosen
    npso, niter = 100, 200
    SimplePSO(lambda x:rosen(x.T), 2 * np.random.rand(npso, 2), niter=niter)
    """
    import numpy as np
    from numpy.random import rand

    x = x0
    m, n = x0.shape

    y = func(x)
    ix = np.argmin(y)
    x_pb = x  # shape(m, n)
    y_pb = y  # shape(m,)
    x_gb = x[ix]  # shape(n,)
    y_gb = y[ix]  # shape()
    y_gb_list = np.empty(niter, 'float')
    i_gb_list = np.empty(niter, 'float')

    for i in range(niter):
        x = x + 2 * (rand(m, n) * (x_pb - x) + rand(m, n) * (x_gb - x))
        y = func(x)

        ix = (y <= y_pb)
        if ix.any():
            y_pb[ix] = y[ix]
            x_pb[ix] = x[ix]
        ix = np.argmin(y)
        if y[ix] <= y_gb:
            x_gb = x[ix]
            y_gb = y[ix]

        y_gb_list[i] = y_gb
        i_gb_list[i] = ix

    return x_gb, y_gb, y_gb_list, i_gb_list
