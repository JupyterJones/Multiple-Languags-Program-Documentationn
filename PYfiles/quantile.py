def quantile(a, q=None, nsig=None, weights=None, sorted=False, nmin=0):
    '''
    nmin: int
        Set `nmin` if you want a more reliable result. 
        Return `nan` when the tail probability is less than `nmin/a.size`.
    '''
    import numpy as np
    from scipy.stats import norm
    
    a = np.asarray(a)
    assert a.ndim == 1
    if weights is None:
        if not sorted:
            a = np.sort(a)
        pcum = np.arange(0.5, a.size)/a.size
    else:
        w = np.asarray(weights)
        assert a.shape == w.shape
        if not sorted:
            ix = np.argsort(a)
            a, w = a[ix], w[ix]
        pcum = (np.cumsum(w) - 0.5 * w)/np.sum(w)
    
    if q is None:
        if nsig is None:
            raise ValueError('One of `q` and `nsig` should be specified.')
            #q = norm.cdf([0, -1, 1, -2, 2, -3, 3])
        else:
            q = norm.cdf(nsig)
    else:
        q = np.asarray(q)
    
    if len(a):
        res = np.interp(q, pcum, a)
    else:
        res = np.full_like(q, np.nan, dtype='float')

    if nmin is not None:
        ix = np.fmin(q, 1 - q) * a.size < nmin
        if not np.isscalar(res):
            res[ix] = np.nan
        elif ix:
            res = np.nan
    return res
    
    
def conflevel(p, q=None, nsig=None, weights=None, sorted=False):
    '''
    used for 2d contour.
    '''
    import numpy as np
    from scipy.stats import norm
    
    p = np.asarray(p).reshape(-1)
    if weights is None:
        if not sorted:
            p = np.sort(p)[::-1]
        pw = p
    else:
        w = np.asarray(weights).reshape(-1)
        assert p.shape == w.shape
        if not sorted:
            ix = np.argsort(p)[::-1]
            p, w = p[ix], w[ix]
        pw = p*w
    pcum = (np.cumsum(pw) - 0.5 * pw)/np.sum(pw)
    
    if q is None:
        if nsig is None:
            raise ValueError('One of `q` and `nsig` should be specified.')
            #q = norm.cdf([0, -1, 1, -2, 2, -3, 3])
        else:
            q = 2 * norm.cdf(nsig) - 1
    else:
        q = np.asarray(q)
    
    if len(p):
        res = np.interp(q, pcum, p)
    else:
        res = np.empty_like(q, np.nan, dtype='float')
    return res

    