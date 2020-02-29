import matplotlib.gridspec as gd
import matplotlib.pyplot as plt
import numpy as np
from markovitz import MarkowitzBullet
from capm import CAPM


class PyfolioEngine:
    def __init__(self, data, expected_mean, risk_free_return, **kwargs):
        # Data
        self.data = data
        # self.ret_matrix, self.cov_matrix = mean_and_cov_matrix(self.data)

        # This calculates the mean vector
        returns_daily = data.pct_change()
        self.ret_matrix = np.array(returns_daily.mean() * 250)

        # This calculates the covariance matrix
        cov_daily = returns_daily.cov()
        self.cov_matrix = np.array(cov_daily * 250)

        # Markowitz bullet
        marko = kwargs.get('marko', dict())
        self.marko = MarkowitzBullet(self.ret_matrix, self.cov_matrix, expected_mean, **marko)

        # capital assets pricing model
        cap = kwargs.get('cap', dict())
        self.capm = CAPM(self.ret_matrix, self.cov_matrix, expected_mean, risk_free_return, **cap)

    def plot(self):
        # Figure
        fig = plt.figure()
        fig.canvas.set_window_title('Portfolio optimization')

        # Grid
        gs = gd.GridSpec(1, 2, figure=fig)

        # Markowitz bullet
        ax1 = fig.add_subplot(gs[0, :1])
        self.marko.plot(ax1)

        # Capital Assets Pricing Model
        ax2 = fig.add_subplot(gs[0, 1:])
        self.marko.plot(ax2, line_only=True)
        self.capm.plot(ax2)

        # Show plot
        plt.show()
