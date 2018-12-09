import matplotlib.pyplot as plt
import numpy as np
def makegausskernel(xsig, ysig, dx, dy, nsig=4):
    """nbin ~ nsig * xsig / dx
    kernel shape: 2 * nbinx + 1 where nbinx + 0.5 >= nsig * xsig / dx
    Examples
        plt.imshow(make_gauss_kernel(0.05, 0.05, 0.01, 0.01, 3.5))
    """
    from scipy.stats import norm

    nbins_x = np.int32(np.ceil(nsig * xsig / dx - 0.5))
    nbins_y = np.int32(np.ceil(nsig * ysig / dy - 0.5))

    xbins = np.arange(-nbins_x - 0.5, nbins_x + 1) * dx
    ybins = np.arange(-nbins_y - 0.5, nbins_y + 1) * dy

    p_x = np.diff(norm.cdf(xbins, scale=xsig))
    p_y = np.diff(norm.cdf(ybins, scale=ysig))

    # make correction as the left side has better accuracy
    p_x[-nbins_x:] = p_x[nbins_x - 1::-1]
    p_y[-nbins_y:] = p_y[nbins_y - 1::-1]
    # p_x[:nbins_x] = p_x[-1:-nbins_x - 1:-1]
    # p_y[:nbins_y] = p_y[-1:-nbins_y - 1:-1]

    p = p_x * p_y[:, None]
    return p / p.sum()
#makegausskernel(0.05, 0.05, 0.01, 0.01, 3.5)