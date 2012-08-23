import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
from mpl_toolkits.axes_grid1 import make_axes_locatable
import numpy as np
from linregress import LinearRegression


def _updatecopy(new, old):
    d = old.copy()
    d.update(new)
    return d


def _clean(z):
    return z[np.isfinite(z)]


class MarginalHistScatter(object):
    def __init__(self, ax=None, hist_size=0.6, pad=0.05, figsize=(15, 8)):

        # make a new fig/axes if needed
        if ax is None:
            self.fig = plt.figure(figsize=figsize)
            self.scatter_ax = fig.add_subplot(111)

        else:
            self.scatter_ax = ax
            self.fig = ax.figure

        self.divider = make_axes_locatable(self.scatter_ax)

        self.scatter_ax = ax
        if self.scatter_ax:
           self.fig = self.scatter_ax.figure
        else:
            self.fig = None
        self.top_hists = []
        self.right_hists = []
        self.hist_size = hist_size
        self.pad = pad
        self.xfirst_ax = None
        self.yfirst_ax = None


    def append(self, x, y, scatter_kwargs, hist_kwargs,
            add_regression=False, regression_kwargs=None, num_ticks=3):
        """
        `x` and `y` are the data to use

        `scatter_kwargs` configure the scatter; `hist_kwargs` configure the
        corresponding marginal hists.

        `add_regression` will add a regression line to the scatter, configured
        by `regression_kwargs`.

        `num_ticks` sets how many tick marks to use
        """
        regression_kwargs = regression_kwargs or {}
        scatter_kwargs = scatter_kwargs or {}
        hist_kwargs = hist_kwargs or {}

        # Plot the scatter
        self.scatter_ax.scatter(x, y, **scatter_kwargs)

        # provided hist_kwargs will be updated with these additional kwargs:
        xhist_kwargs = dict()
        yhist_kwargs = dict(orientation='horizontal')

        xhk = _updatecopy(hist_kwargs, xhist_kwargs)
        yhk = _updatecopy(hist_kwargs, yhist_kwargs)

        axhistx = self.divider.append_axes('top', size=self.hist_size,
                pad=self.pad, sharex=self.scatter_ax, sharey=self.xfirst_ax)

        axhisty = self.divider.append_axes('right', size=self.hist_size,
                pad=self.pad, sharey=self.scatter_ax, sharex=self.yfirst_ax)

        axhistx.yaxis.set_major_locator(
                MaxNLocator(nbins=num_ticks, prune='both'))
        axhisty.xaxis.set_major_locator(
                MaxNLocator(nbins=num_ticks, prune='both'))

        if not self.xfirst_ax:
            self.xfirst_ax = axhistx
        if not self.yfirst_ax:
            self.yfirst_ax = axhisty

        # keep track of which axes are which, because looking into fig.axes
        # list will get awkward....
        self.top_hists.append(axhistx)
        self.right_hists.append(axhisty)

        # scatter will deal with NaN, but hist will not.  So clean the data
        # here.
        hx = _clean(x)
        hy = _clean(y)

        # Only plot hists if there's valid data
        if len(hx) > 0:
            axhistx.hist(hx, **xhk)
        if len(hy) > 0:
            axhisty.hist(hy, **yhk)

        # Unsure about whether this should be here . . . a nice touch, but
        # should prob be left to the user
        axhistx.legend(loc='best', frameon=False, prop=dict(size=10))

        # Turn off unnecessary labels -- for these, use the scatter's axes
        # labels
        for txt in axhisty.get_yticklabels() + axhistx.get_xticklabels():
            txt.set_visible(False)

        for txt in axhisty.get_xticklabels():
            txt.set_rotation(-90)

        # Add regression lines if requested
        if add_regression:
            lm = LinearRegression(x=xi, y=yi, formula='y~x')
            xr = np.array([min(hx), max(hx)])
            yr = lm.slope * xr + lm.intercept
            try:
                color = scatter_kwargs['c']
            except KeyError:
                color = 'k'
            self.scatter_ax.plot(xr, yr, color=color, **regression_kwargs)


if __name__ == "__main__":
    import numpy as np
    x1 = np.random.normal(0, 0.5, 1000)
    y1 = np.random.normal(0, 0.5, 1000)

    x2 = np.random.normal(0.5, 0.5, 500)
    y2 = (np.random.normal(0.2, 0.1, 500))

    fig = plt.figure()
    ax1 = fig.add_subplot(111)

    m = MarginalHistScatter(ax1)
    m.append(x1, y1,
            scatter_kwargs=dict(c='k', linewidths=0, alpha=0.5, marker='.'),
            hist_kwargs=dict(label='all', color='k', alpha=0.5, bins=20))
    m.append(x2, y2,
            scatter_kwargs=dict(c='r', alpha=0.5),
            hist_kwargs=dict(label='subset', color='r', bins=20))

    plt.show()
