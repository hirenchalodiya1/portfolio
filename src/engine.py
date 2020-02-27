"""
This engine single-handedly handles the portfolio optimsation task
It requires only the general parameters and can be tweaked according to the user, and
it returns the desired results.
Signed off: Hiren Chalodiya <chalodiya.1@iitj.ac.in>
            Mayank Raj <raj.6@iitj.ac.in>
"""
import matplotlib.gridspec as gd
import matplotlib.pyplot as plt
from markovitz import MarkowitzBullet
import numpy as np


class PyfolioEngine:
    def __init__(self, data, expected_mean, risk_free_return, **kwargs):
        # Data
        self.data = data

        # This calculates the mean vector
        returns_daily = data.pct_change()
        self.ret_matrix = np.array(returns_daily.mean() * 250)
        
        # This calculates the covariance matrix
        cov_daily = returns_daily.cov()
        self.cov_matrix = np.array(cov_daily * 250)
        
        # Markowitz bullet
        # This calls a function which plots the markowitz bullet
        marko = {}
        if kwargs.get('marko_mu_min'): marko['mu_min'] = kwargs.get('marko_mu_min')
        if kwargs.get('marko_mu_max'): marko['mu_max'] = kwargs.get('marko_mu_max')
        if kwargs.get('marko_mu_gap'): marko['mu_gap'] = kwargs.get('marko_mu_gap')
        self.marko = MarkowitzBullet(self.ret_matrix, self.cov_matrix, expected_mean, **marko)


        print()
        print('----------------------------------------------------------')
        print('The weights as obtained from the portfolio for 25 stocks')
        print('----------------------------------------------------------')
        keys = data.keys()
        ws = self.marko.w
        # print(self.marko.w)
        for id_, k in enumerate(zip(keys, ws)):
            print('{} :{} --> {:.6f}'.format(id_+1, k[0], k[1]))
        print('----------------------------------------------------------')

    def plot(self):
        # Figure
        fig = plt.figure()
        fig.canvas.set_window_title('Portfolio optimization')
        
        # Grid
        gs = gd.GridSpec(1, 1, figure=fig)

        # Markowitz bullet
        ax1 = fig.add_subplot(gs[0, :])
        self.marko.plot(ax1)
        
        # Show plot
        plt.show()
