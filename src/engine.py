import matplotlib.gridspec as gd
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from markovitz import MarkowitzBullet
from capm import CAPM
from betas import Betas, NewBetas


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

        # Capital assets pricing model
        cap = kwargs.get('cap', dict())
        self.capm = CAPM(self.ret_matrix, self.cov_matrix, expected_mean, risk_free_return, **cap)

        # Betas
        # For market ret and weights matrix for SML, beta calculation
        # We use derived portfolio value so we need to devied ret_risky and w_risky by sum(w_risky)
        market_weights = pd.DataFrame(pd.Series(self.capm.w_risky / sum(self.capm.w_risky), index=data.keys()))
        daily_return_of_market = (returns_daily * market_weights[0]).sum(1)

        # Prepare new betas
        new_returns = kwargs.get('new', {}).get('data', {})
        new_returns_daily = new_returns.pct_change()
        self.new_betas = NewBetas(new_returns_daily, daily_return_of_market, risk_free_return)
        _b = self.new_betas.betas.values()
        if not _b:
            _b_max = 1
            _b_min = 0
        else:
            _b_max = max(_b)
            _b_min = min(_b)

        # First calculate new beta so that graph can ploted nicely
        self.betas = Betas(returns_daily,
                           daily_return_of_market,
                           self.capm.ret_risky / sum(self.capm.w_risky),
                           risk_free_return,
                           self.ret_matrix, beta_max=_b_max, beta_min=_b_min)

    def plot(self, show_marko=True, show_capm=True, show_beta=True):
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

        if show_beta:
            # Part 3
            # Figure
            fig3 = plt.figure()
            fig3.canvas.set_window_title('Security Market Line')

            # Grid
            gs3 = gd.GridSpec(1, 1, figure=fig3)

            # plot
            ax3 = fig3.add_subplot(gs3[:, :])
            self.betas.plot(ax3)
            self.new_betas.plot(ax3)

        # Show plot
        plt.show()

    def pprint(self, show_marko=True, show_capm=True, show_beta=True):
        if show_marko:
            print('-----------------------------------------------------------------------------------')
            print('Weights for desired portfolio ( w/o risk free ) | Markowitz Theory                 ')
            print('-----------------------------------------------------------------------------------')
            for i, j in enumerate(zip(self.data.keys(), self.marko.w), 1):
                print('{:2} : {:10s} --> {:10.6f}'.format(i, j[0], j[1]))
            print('-----------------------------------------------------------------------------------')
            print('Observations: ')
            print('1. For given return {:.2f}% minimum risk is {:.2f}%'.format(self.marko.ret * 100, self.marko.risk * 100))
            print()

        if show_capm:
            print('-----------------------------------------------------------------------------------')
            print('Weights for desired portfolio ( with risk free ) | Capital Assets Pricing Model    ')
            print('-----------------------------------------------------------------------------------')
            print('{:2} : {:10s} --> {:10.6f}'.format(1, 'Risk Free', self.capm.w_risk_free))
            for i, j in enumerate(zip(self.data.keys(), self.capm.w_risky), 2):
                print('{:2} : {:10s} --> {:10.6f}'.format(i, j[0], j[1]))
            print('-----------------------------------------------------------------------------------')
            print('Observations: ')
            print('1. For given return {:.2f}% minimum risk is {:.2f}%'.format(self.capm.ret * 100, self.capm.risk * 100))
            print('2. In given portfolio for {:.2f}% return obtained by market while, '.format(self.capm.ret_risky * 100))
            print('   {:.2f}% return obtained by risk free assets'.format((self.capm.ret - self.capm.ret_risky) * 100))
            print('3. μ = {:.3f} σ + {:.3f}'.format(self.capm.slope, self.capm.RR))

        if show_beta:
            print('-----------------------------------------------------------------------------------')
            print('     Stock Code    Beta        Return from SML Line   Actual return                     ')
            print('-----------------------------------------------------------------------------------')
            for i, j in enumerate(zip(self.betas.betas.items(), self.betas.MM), 1):
                print('{:2} : {:10s} -> {:10.6f} {:15.2f} {:15.2f}'.format(i, j[0][0], j[0][1], self.betas.line_sml(j[0][1]), j[1]))
            print('-----------------------------------------------------------------------------------')
            print('Observations: ')
            print('1. Return from SML Line and actual return are same')
