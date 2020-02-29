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

    def plot(self, show_marko=True, show_capm=True):
        """
        fig1: Markowitz bullet Figure
        fig2: Capital market line
        """
        # Part 1
        if show_marko:
            # Figure
            fig1 = plt.figure()
            fig1.canvas.set_window_title('Markowitz bullet')

            # Grid
            gs1 = gd.GridSpec(1, 1, figure=fig1)

            # plot
            ax1 = fig1.add_subplot(gs1[:, :])
            self.marko.plot(ax1)

        if show_capm:
            # Part 2
            # Figure
            fig2 = plt.figure()
            fig2.canvas.set_window_title('Capital assets pricing model')

            # Grid
            gs2 = gd.GridSpec(1, 1, figure=fig2)

            # plot
            ax2 = fig2.add_subplot(gs2[:, :])
            self.marko.plot(ax2, gp=100, line_only=True)
            self.capm.plot(ax2)

        # Show plot
        plt.show()

    def pprint(self):
        print('-------------------------------------------------------')
        print('Weights for desired portfolio ( w/o risk free )        ')
        print('-------------------------------------------------------')
        for i, j in enumerate(zip(self.data, self.marko.w), 1):
            print('{:2} : {:6s} --> {:.6f}'.format(i, j[0], j[1]))
        print('-------------------------------------------------------')
