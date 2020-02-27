import matplotlib.gridspec as gd
import matplotlib.pyplot as plt
from utils import mean_and_cov_matrix
from markovitz import MarkowitzBullet
from capm import CAPM
import numpy as np


class PyfolioEngine:
    def __init__(self, data, expected_mean, risk_free_return, **kwargs):
        # Data
        self.data = data
        # self.ret_matrix, self.cov_matrix = mean_and_cov_matrix(self.data)
        returns_daily = data.pct_change()
        self.ret_matrix = np.array(returns_daily.mean() * 250)
        
        cov_daily = returns_daily.cov()
        self.cov_matrix = np.array(cov_daily * 250)
        
        # Markowitz bullet
        marko = {}
        if kwargs.get('marko_mu_min'): marko['mu_min'] = kwargs.get('marko_mu_min')
        if kwargs.get('marko_mu_max'): marko['mu_max'] = kwargs.get('marko_mu_max')
        if kwargs.get('marko_mu_gap'): marko['mu_gap'] = kwargs.get('marko_mu_gap')
        self.marko = MarkowitzBullet(self.ret_matrix, self.cov_matrix, expected_mean, **marko)

        # capital assets pricing model
        cap = {}
        if kwargs.get('cap_mu_min'): cap['mu_min'] = kwargs.get('cap_mu_min')
        if kwargs.get('cap_mu_max'): cap['mu_max'] = kwargs.get('cap_mu_max')
        if kwargs.get('cap_mu_gap'): cap['mu_gap'] = kwargs.get('cap_mu_gap')
        # self.capm = CAPM(self.ret_matrix, self.cov_matrix, expected_mean, risk_free_return, **cap)


    def plot(self):
        # Figure
        fig = plt.figure()
        fig.canvas.set_window_title('Portfolio optimization')
        
        # Grid
        gs = gd.GridSpec(1, 2, figure=fig)

        # Markowitz bullet
        ax1 = fig.add_subplot(gs[0, :])
        self.marko.plot(ax1)
        
        # Capital Assets Pricing Model 
        # ax2 = fig.add_subplot(gs[0, 1:])
        # self.marko.plot(ax2)
        # self.capm.plot(ax2)
        
        # Show plot
        plt.show()